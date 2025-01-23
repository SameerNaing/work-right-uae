import re

from app.core.config import llm


def _faq_rephase_prompt(topic, question, answer):
    system_prompt = """
    You are an intellengent rephaser. 
    Rephrase the following answer with the question and topic as necessary to make the answer contextually complete.
    Only one rephased answer is enough with no extra text and do not add questions in the answer.
    Strickly follow the output format.

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


def rephase(topics, questions, answers):
    result = []

    for topic, question, answer in zip(topics, questions, answers):
        prompt = _faq_rephase_prompt(topic, question, answer)
        res = llm.complete(prompt)
        res = re.sub(r"\s+", " ", res.text).strip()
        result.append(res.choices[0].text.strip())

    return result
