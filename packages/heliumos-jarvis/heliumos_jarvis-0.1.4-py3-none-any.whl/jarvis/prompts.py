from langchain.prompts import PromptTemplate

PREFIX = """You are a friendly Assistant that having a conversation with a human. You NEVER \
answer that you are an AI language model. If you don't know the answer truthfully \
say you don't have an answer. Don't make up an answer.
You should think step by step.

TOOLS:
------

You has access to the following tools:"""

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, \
or there is not a available tool for using, you MUST use the format:

```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```"""

SUFFIX = """Begin!
Previous conversation history:
{chat_history}


(You do not need to use these pieces of information if not relevant)

You MUST always respond to me in {language}. 
If the response is not {language}, You should translate it to {language}.
You should think step by step.

Human: {input}
{agent_scratchpad}"""

_summary_map_prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
SUMMARY_MAP_PROMPT = PromptTemplate(template=_summary_map_prompt_template, input_variables=["text"])

_summary_combine_prompt_template = """Combine these summaries:
"{text}"
COMBINED SUMMARY:"""
SUMMARY_COMBINE_PROMPT = PromptTemplate(template=_summary_combine_prompt_template, input_variables=["text"])

_translate_prompt_template = """You are professional Translator to translate following text to {language}.

{input}"""
TRANSLATE_PROMPT = PromptTemplate(template=_translate_prompt_template, input_variables=["input", "language"], )

_MATH_PROMPT_TEMPLATE = """
Please use the following format to Translate a math problem into a expression that can be executed using Python's numexpr library. \
Use the output of running this code to answer the question.


Question: ${{Question with math problem.}}
```text
${{single line mathematical expression that solves the problem}}
```
...numexpr.evaluate(text)...
```output
${{Output of running the code}}
```
Answer: ${{Answer}}

Begin.

Question: Compare 37593 ** -0.1 and 67?
```text
37593 ** -0.1 > 67
```
...numexpr.evaluate("37593 ** -0.1 > 67")...
```output
False
```
Answer: 37593 ** -0.1 < 67

Question: What is 334?
```text
334
```
...numexpr.evaluate("334")...
```output
334
```
Answer: 334

Question: What is 37593 + 67?
```text
37593 + 67
```
...numexpr.evaluate("37593 + 67")...
```output
37660
```
Answer: 37660

Question: What is 37593 ** -0.1?
```text
37593 ** -0.1
```
...numexpr.evaluate("37593 ** -0.1")...
```output
0.348729993
```
Answer: 0.348729993

Question: What is 37593 + 1.675621?
```text
37593 + 1.675621
```
...numexpr.evaluate("37593 + 1.675621")...
```output
37594.675621
```
Answer: 37594.675621

Question: What is 37593 * 67?
```text
37593 * 67
```
...numexpr.evaluate("37593 * 67")...
```output
2518731
```
Answer: 2518731

Question: 37593^(1/5)
```text
37593**(1/5)
```
...numexpr.evaluate("37593**(1/5)")...
```output
8.222831614237718
```
Answer: 8.222831614237718

Question: {question}
"""

MATH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=_MATH_PROMPT_TEMPLATE,
)
