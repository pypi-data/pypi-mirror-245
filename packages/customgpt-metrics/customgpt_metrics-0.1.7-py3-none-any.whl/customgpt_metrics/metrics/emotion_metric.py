from .base_metric import BaseMetric
from .model_provider import model_provider
import json

emotion_prompt = "Given a user message and response, analyze the user-query and categorize it strictly as " \
                 "one of the five sentiments: positive, neutral, confusion, dissatisfaction or frustration. " \
                 "Use the tone and intent of the user-query too."

emotion_schema = {
    "type": "object",
    "properties": {
        "emotion_check": {"type": "string",
                          "enum": ["positive", "neutral", "confusion", "dissatisfaction", "frustration"]},
    },
    "required": ["emotion_check"]
}


class EmotionMetric(BaseMetric):
    key = 'emotion' 
    def __init__(self, api_key, base_url, model, model_provider='openai'):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model
        self.model_provider = model_provider

    def evaluate(self, chat):
        try:
            system_message = emotion_prompt
            conversation = f"user-query:\n {chat.user_query} \nbot-response:\n {chat.openai_response}"

            messages = [
                {"role": "user", "content": system_message},
                {"role": "user", "content": conversation},
            ]

            functions = [{"name": "emotion_schema", "parameters": emotion_schema}]
            function_call = {"name": "emotion_schema"}

            chat_response = model_provider.chat_completion(api_key=self.api_key,
                                                           base_url=self.base_url,
                                                           model_provider=self.model_provider,
                                                           model=self.model,
                                                           messages=messages,
                                                           functions=functions,
                                                           function_call=function_call,
                                                           temperature=0,
                                                           max_tokens=256,
                                                           top_p=1,
                                                           frequency_penalty=0.0,
                                                           presence_penalty=0.0)
            function_response = chat_response.choices[0].message.function_call.arguments
            parsed_response = json.loads(function_response)

            return parsed_response['emotion_check']
        except Exception as e:
            return f"Failed to evaluate EmotionMetric::evaluate::{e}"