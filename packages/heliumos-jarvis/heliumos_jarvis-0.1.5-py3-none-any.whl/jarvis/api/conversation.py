import json
from typing import (
    List,
    Optional,
)

from fastapi import APIRouter
from langchain.agents import AgentExecutor, ConversationalAgent, Tool, Agent
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory, VectorStoreRetrieverMemory
from langchain.memory import ReadOnlySharedMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.schema.vectorstore import VectorStoreRetriever
from langchain.vectorstores import Milvus
from pydantic import BaseModel

from jarvis.jarvis_configuration import settings
from jarvis.memories import JarvisSummaryBufferMemory
from jarvis.prompts import PREFIX, SUFFIX, FORMAT_INSTRUCTIONS, MATH_PROMPT
from jarvis.stores import Memory
from jarvis.stores import ToolInstance
from jarvis.tools.calculator import JarvisSimpleMath
from . import llm, embeddings, tool_instance_store, memory_store, message_history_store
from ..memories.vector_store import JarvisVectorStoreRetrieverMemory
from ..vectorstores.milvus import JarvisMilvus

router = APIRouter()


class Knowledge(BaseModel):
    id: str
    name: str
    description: str


class ToolInstanceUsage(BaseModel):
    tool_instance_id: str
    usage_name: str
    usage_condition: str


class ConversationRequest(BaseModel):
    input: str
    language: Optional[str] = "Chinese"
    human_name: Optional[str] = ""
    character_id: str
    memory_id: Optional[str] = None
    used_tools: List[ToolInstanceUsage]


class ConversationResponse(BaseModel):
    message: str


def _create_or_get_memory(memory: Memory) -> BaseChatMemory:
    history_memory = ConversationBufferWindowMemory(
        input_key="input",
        memory_key="chat_history",
        k=0
    )
    if memory is None:
        return history_memory

    if memory.memory_type == "SUMMARY_BUFFER":
        memory_init_params = json.loads(memory.memory_init_params)
        history_memory = JarvisSummaryBufferMemory(
            llm=llm,
            input_key="input",
            memory_key="chat_history",
            max_token_limit=memory_init_params["summary_threshold"],
            session_id=memory.id,
            message_store=message_history_store,
            return_messages=True
        )
    elif memory.memory_type == "VECTOR_STORE":
        vector_store = JarvisMilvus(
            embedding_function=embeddings,
            collection_name="JARVIS_MEMORY",
            drop_old=False,
            connection_args={
                "host": settings.MILVUS_HOST,
                "port": settings.MILVUS_PORT,
                "db_name": settings.MILVUS_DB,  # "default",
                "user": settings.MILVUS_USERNAME,  # "cdgouicgkz",
                "password": settings.MILVUS_PASSWORD,  # "YxX777FA0sT2rT4C",
            },
            partition_key="memory_id"
        )
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 8,
                "fetch_k": 32,
                "expr": f"memory_id==\"{memory.id}\"",
            },


        )
        history_memory = JarvisVectorStoreRetrieverMemory(
            memory_id=memory.id,
            retriever=retriever,
            input_key="input",
            memory_key="chat_history",
            return_messages=True,
            exclude_input_keys=["language"],
        )
    # 会话有两种：第一种是长期会话，需要将内容记录到向量数据库中用于后续查询。第二种是短期会话，会话结束后不会内容不会保存到向量数据库中

    return history_memory


def _get_knowledge_vector_store(knowledge_id: str) -> VectorStoreRetriever:
    vector_store = JarvisMilvus(
        embedding_function=embeddings,
        collection_name="JARVIS_KNOWLEDGE",
        connection_args={
            "host": settings.MILVUS_HOST,
            "port": settings.MILVUS_PORT,
            "db_name": settings.MILVUS_DB,  # "default",
            "user": settings.MILVUS_USERNAME,  # "cdgouicgkz",
            "password": settings.MILVUS_PASSWORD,  # "YxX777FA0sT2rT4C",
        },
        partition_key="knowledge_id"
    )
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 32,
            "expr": f"knowledge_id==\"{knowledge_id}\"",
            # "param": {
            #     "metric_type": "L2", "params": {
            #         # search for vectors with a distance smaller than 10.0
            #         "radius": 3.0,
            #         # filter out vectors with a distance smaller than or equal to 5.0
            #         "range_filter": 0.0
            #     }
            # }
        }
    )
    return retriever


def _load_build_in_tool(tool_instance: ToolInstance, tool_usage: ToolInstanceUsage,
                        history_memory: BaseChatMemory) -> Optional[Tool]:
    if tool_instance.tool_name.upper() == "CALCULATOR":
        llm_math_chain = JarvisSimpleMath.from_llm(llm=llm, prompt=MATH_PROMPT, verbose=True)
        return Tool(
            name=tool_usage.usage_name,
            description=tool_usage.usage_condition,
            func=llm_math_chain.run,
        )
    elif tool_instance.tool_name.upper() == "RETRIEVE":
        knowledge_id = tool_instance.instance_parameters["knowledge_id"]
        return _build_knowledge_tool(knowledge_id, tool_usage.usage_name, tool_usage.usage_condition, history_memory)
    return None


def _build_knowledge_tool(knowledge_id: str, usage_name: str, usage_condition: str, history_memory: BaseChatMemory):
    retriever = _get_knowledge_vector_store(knowledge_id)
    read_only_memory = ReadOnlySharedMemory(memory=history_memory)
    conversation_knowledge_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        rephrase_question=False,
        retriever=retriever,
        verbose=True,
        chain_type="stuff",
        memory=read_only_memory,
    )
    knowledge_tool = Tool(
        name=usage_name,
        description=usage_condition,
        func=conversation_knowledge_chain.run,
    )
    return knowledge_tool


def _generate_agent(history_memory: BaseChatMemory, tools: List[Tool]) -> Agent:
    agent = ConversationalAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        verbose=True,
        memory=history_memory,
        input_variables=["input", "agent_scratchpad", "chat_history", "language"],
        early_stopping_method='force',
        prefix=PREFIX,
        suffix=SUFFIX,
        format_instructions=FORMAT_INSTRUCTIONS,
    )
    agent.llm_chain.verbose = True
    return agent


@router.post("/conversation")
async def converse(conversationRequest: ConversationRequest):
    # 通过
    memory = None
    if conversationRequest.memory_id is not None and memory_store.exist_by_id(memory_id=conversationRequest.memory_id):
        memory = memory_store.get_by_id(conversationRequest.memory_id)

    history_memory = _create_or_get_memory(memory)
    # 会话有两种：第一种是长期会话，需要将内容记录到向量数据库中用于后续查询。第二种是短期会话，会话结束后不会内容不会保存到向量数据库中

    tools = []
    for tool_usage in conversationRequest.used_tools:
        tool_instance = tool_instance_store.get_instance_by_id(tool_usage.tool_instance_id)
        _build_in_tool = _load_build_in_tool(tool_instance, tool_usage, history_memory)
        tools.append(_build_in_tool)
    agent = _generate_agent(history_memory=history_memory, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        # max_iterations=3,
        memory=history_memory,
        handle_parsing_errors="respond to user: I can not answer the question for now",

    )
    try:
        out = await agent_executor.arun(
            input=conversationRequest.input,
            language=conversationRequest.language,
        )
    finally:
        pass
    return ConversationResponse(message=out)
