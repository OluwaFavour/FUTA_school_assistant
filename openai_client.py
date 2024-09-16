from time import sleep
from openai import OpenAI
from openai.types.fine_tuning import FineTuningJob


class OpenAIClient:
    def __init__(
        self,
        api_key: str,
        organization: str,
        project: str,
        model: str,
        max_tokens: int = 300,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key,
            organization=organization,
            project=project,
        )
        self.model = model
        self.max_tokens = max_tokens

    def upload_training_data(self, training_file: str) -> str | dict[str, str]:
        try:
            file_reader = open(training_file, "rb")
            file = self.client.files.create(file=file_reader, purpose="fine-tune")
            return file.id
        except OSError as e:
            return {"error": f"Error reading file. {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

    def create_fine_tuned_model(
        self, file_id: str, suffix: str = "futa-soc-assistant"
    ) -> FineTuningJob | dict[str, str]:
        try:
            response = self.client.fine_tuning.jobs.create(
                training_file=file_id,
                model=self.model,
                suffix=suffix,
            )
            return response.id
        except Exception as e:
            return {"error": str(e)}

    def get_fine_tuned_model(self, job_id: str) -> FineTuningJob | dict[str, str]:
        try:
            response = self.client.fine_tuning.jobs.retrieve(job_id)
            return response
        except Exception as e:
            return {"error": str(e)}

    def is_job_complete(self, job_id: str) -> bool:
        initial_status = self.get_fine_tuned_model(job_id).status
        if initial_status == "succeeded":
            print("Job succeeded")
            return True
        elif initial_status == "failed":
            return True
        elif initial_status == "cancelled":
            return True
        else:
            return False

    def is_job_successful(self, job_id: str) -> bool:
        if self.is_job_complete(job_id):
            return self.get_fine_tuned_model(job_id).status == "succeeded"
        else:
            return False

    def check_job_success(self, job_id: str) -> bool:
        is_job_successful = self.is_job_successful(job_id)
        if is_job_successful:
            return True
        retry_count = 0
        while not is_job_successful:
            if retry_count >= 10:
                return False
            is_job_successful = self.is_job_successful(job_id)
            if is_job_successful:
                return True
            print("Job not successful. Retrying in 6 seconds...")
            sleep(6)
            retry_count += 1

    def ask_question(self, messages: list[dict[str, str]]) -> str:
        prompt_messages = [
            {
                "role": "system",
                "content": "You are a chatbot that answers factual questions related to the School of Computing at FUTA only, other questions should not be answered.",
            }
        ]
        prompt_messages.extend(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt_messages,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e
