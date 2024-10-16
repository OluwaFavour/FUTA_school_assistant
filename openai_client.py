from openai import OpenAI


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

    def _create_prompt(
        self, role: str, content: str, messages: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        """Creates a full prompt message for the chatbot."""
        system_message = {"role": role, "content": content}
        return [system_message] + messages

    def _get_response(self, model: str, messages: list[dict[str, str]]) -> str:
        """Handles the interaction with the OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to get response: {e}")

    def ask_soc_question(self, messages: list[dict[str, str]]) -> str:
        prompt_messages = self._create_prompt(
            role="system",
            content="You are a chatbot that answers factual questions related to the School of Computing at FUTA only, other questions should not be answered.",
            messages=messages,
        )
        return self._get_response(model=self.soc_model, messages=prompt_messages)

    def ask_admission_question(self, messages: list[dict[str, str]]) -> str:
        prompt_messages = self._create_prompt(
            role="system",
            content="You are a chatbot that only answers factual questions related to enquries on admission into Federal University of Technology, Akure (FUTA). Other questions should not be answered.",
            messages=messages,
        )
        return self._get_response(model=self.admission_model, messages=prompt_messages)
