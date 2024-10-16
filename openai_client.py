from time import sleep
from openai import OpenAI
from openai.types.fine_tuning import FineTuningJob


class OpenAIClient:
    def __init__(
        self,
        api_key: str,
        organization: str,
        project: str,
        soc_model: str,
        admission_model: str,
        max_tokens: int = 300,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key,
            organization=organization,
            project=project,
        )
        self.soc_model = soc_model
        self.admission_model = admission_model
        self.max_tokens = max_tokens

    def ask_soc_question(self, messages: list[dict[str, str]]) -> str:
        prompt_messages = [
            {
                "role": "system",
                "content": "You are a chatbot that answers factual questions related to the School of Computing at FUTA only, other questions should not be answered.",
            }
        ]
        prompt_messages.extend(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.soc_model,
                messages=prompt_messages,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e

    def ask_admission_question(self, messages: list[dict[str, str]]) -> str:
        prompt_messages = [
            {
                "role": "system",
                "content": "You are a chatbot that answers factual questions related to the Federal University of Technology Akure Admission Enquiry only, other questions should not be answered.",
            }
        ]
        prompt_messages.extend(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.soc_model,
                messages=prompt_messages,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e
