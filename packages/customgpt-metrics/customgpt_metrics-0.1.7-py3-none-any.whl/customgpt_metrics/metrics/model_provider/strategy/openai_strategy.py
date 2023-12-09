import openai
from .model_strategy import ModelStrategy
import time

class OpenAIStrategy(ModelStrategy):
    def __init__(self, api_key, base_url):
        self.default_openai = openai
        self.default_openai.api_key = api_key
        self.default_openai.api_base = base_url
        self.default_openai.api_type = "open_ai"
        self.default_openai.api_version = None

    def chat_completion(self,
                        model,
                        messages,
                        **completion_api_params):
        if not model:
            model = "gpt-3.5-turbo-16k-0613"
        main_model = model
        max_retries = 5
        retry_delay = 5  # in seconds

        for attempt in range(1, max_retries + 1):
            try:
                return self.default_openai.ChatCompletion.create(model=main_model,
                                                                 messages=messages,
                                                                 request_timeout=30,
                                                                 **completion_api_params)
            except Exception as e:
                time.sleep(retry_delay)
