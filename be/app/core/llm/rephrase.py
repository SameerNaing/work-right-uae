import re

from app.core.config import llm


class RephraseManger:
    def __init__(self):
        self.llm = llm

    def _faq_rephrase_prompt(self, topic, question, answer):
        system_prompt = """
        You are an intelligent rephraser.
        Rephrase the following answer with the question and topic as necessary to make the answer contextually complete.
        Only one rephrased answer is enough with no extra text, and do not add questions in the answer.
        Strictly follow the output format.

        Example Input Data:
        Topic: 'General'
        Question: 'Is there a time period for the job offer to be expired?'
        Answer: 'No'

        Example Output Data that you have to generate:
        No, there is no expiry time for the job offer.

        Here is your input
        """
        query_prompt = f"""
        Topic: '{topic}'
        Question: '{question}'
        Answer: '{answer}'
        """
        return f"{system_prompt}{query_prompt}"

    def rephrase_mohre_faq(self, topic, question, answer):
        prompt = self._faq_rephrase_prompt(topic, question, answer)
        res = self.llm.complete(prompt)
        return re.sub(r"\s+", " ", res.text).strip()


rephrase_manager = RephraseManger()
