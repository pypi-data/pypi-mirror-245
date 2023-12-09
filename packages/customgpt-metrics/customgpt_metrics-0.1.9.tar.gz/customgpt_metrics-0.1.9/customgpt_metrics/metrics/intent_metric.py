from .base_metric import BaseMetric
from .model_provider import model_provider
import json

intent_prompt = "Given a user message and response, analyze the user-query and categorize the intent for the " \
                                "user-query as Informational, Navigational, Greetings, Follow-up, Transactional, Troubleshooting " \
                                "and Instructional. Use the bot-response as a reference for better undersrtanding."

intent_schema = {
    "type": "object",
    "properties": {
        "intent_check": {"type": "string",
                         "enum": ["Informational", "Navigational", "Greetings", "Follow-up", "Transactional",
                                  "Troubleshooting", "Instructional"]},
    },
    "required": ["intent_check"]
}


class IntentMetric(BaseMetric):
    key = 'intent'
    def __init__(self, api_key, base_url, model, model_provider='openai'):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model
        self.model_provider = model_provider

    def evaluate(self, chat, model='openai'):
        try:
            system_message = intent_prompt
            conversation = f"user-query:\n{chat.user_query}\nbot-response:\n{chat.openai_response}"

            messages = [
                {"role": "user", "content": system_message},
                {"role": "user", "content": conversation},
            ]

            functions = [{"name": "intent_schema", "parameters": intent_schema}]
            function_call = {"name": "intent_schema"}

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

            return parsed_response['intent_check']

        except Exception as e:
            return f"Failed to evaluate IntentMetric::evaluate::{e}"
