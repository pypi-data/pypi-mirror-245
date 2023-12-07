from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from . import memory_store, gen, message_history_store
from jarvis.exceptions.api_exceptions import JarvisNotFoundException

router = APIRouter()


class MemoryCreation(BaseModel):
    memory_type: str  # BUFFER, SUMMARY_BUFFER, ENTITY, KNOWLEDGE_GRAPH, VECTOR_STORE
    memory_buffer_window: Optional[int] = 3
    summary_threshold: Optional[int] = 256


class MemoryResponse(BaseModel):
    memory_id: str
    memory_type: str  # BUFFER, SUMMARY_BUFFER, ENTITY, KNOWLEDGE_GRAPH, VECTOR_STORE
    memory_buffer_window: int
    summary_threshold: int


@router.post("/memory")
async def create_memory(request: MemoryCreation):
    memory_id = str(next(gen))
    memory_store.add_memory(
        memory_id,
        request.memory_type,
        request.memory_buffer_window,
        request.summary_threshold
    )
    return MemoryResponse(
        memory_id=memory_id,
        memory_type=request.memory_type,
        memory_buffer_window=request.memory_buffer_window,
        summary_threshold=request.summary_threshold
    )


@router.get("/memory/{memory_id}")
async def get_memory_by_id(memory_id: str):
    exists = memory_store.exist_by_id(memory_id)
    if exists is not True:
        raise JarvisNotFoundException(message=f"{memory_id} not found")
    memory = memory_store.get_by_id(memory_id)
    numbers = message_history_store.count_by_session_id(memory_id)
    return {
        "memory_id": memory.id,
        "memory_type": memory.memory_type,
        "memory_buffer_window": memory.memory_buffer_window,
        "summary_threshold": memory.summary_threshold,
        "message_amount": numbers
    }


@router.get("/memory/{memory_id}/messages")
async def get_memory_by_id(memory_id: str):
    exists = memory_store.exist_by_id(memory_id)
    if exists is not True:
        raise JarvisNotFoundException(message=f"{memory_id} not found")
    messages = message_history_store.get_history_by_session_id(memory_id)
    return messages


@router.delete("/memory/{id}")
async def deleteMemoryById():
    pass
