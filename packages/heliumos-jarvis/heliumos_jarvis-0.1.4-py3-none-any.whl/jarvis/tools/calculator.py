from typing import Dict

from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains import LLMMathChain


class JarvisSimpleMath(LLMMathChain):
    def _evaluate_expression(self, expression: str) -> str:
        try:
            return super()._evaluate_expression(expression)
        except Exception as e:
            return "Answer: I can not answer the question"
        # Remove any leading and trailing brackets from the output

    def _process_llm_result(
            self, llm_output: str, run_manager: CallbackManagerForChainRun
    ) -> Dict[str, str]:
        return super()._process_llm_result(llm_output, run_manager)
