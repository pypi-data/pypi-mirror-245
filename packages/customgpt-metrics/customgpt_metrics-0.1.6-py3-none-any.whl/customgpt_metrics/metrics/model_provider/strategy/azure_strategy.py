import openai
from .model_strategy import ModelStrategy


class AzureStrategy(ModelStrategy):
    def __init__(self, api_key, base_url):
        self.azure_openai = openai
        self.azure_openai.api_type = "azure"
        self.azure_openai.api_version = "2023-07-01-preview"
        self.azure_openai.api_base = base_url
        self.azure_openai.api_key = api_key

    def chat_completion(self,
                        model,
                        messages,
                        **completion_api_params):
        if not model:
            model = "gpt-35-turbo-16k"

        max_retries = 1
        retry_delay = 2  # in seconds

        for attempt in range(1, max_retries + 1):
            try:
                return self.azure_openai.ChatCompletion.create(
                    engine=model,
                    messages=messages,
                    **completion_api_params
                )
            except Exception as e:
                time.sleep(retry_delay)
