from .base_metric import BaseMetric
from .model_provider import model_provider
import json

context_prompt = "You are an AI conversation assistant. You are provided with a conversation containing the " \
                 "context used to answer the query, user-query and the bot-response. Your goal is to detect " \
                 "whether the bot was directly able to answer, by understanding the tone and intent of the " \
                 "response.\nIf: the bot is unable to answer, return Out-of-context, Else: return In-context"

context_schema = {
    "type": "object",
    "properties": {
        "context_check": {"type": "string", "enum": ["Out-of-context", "In-context"]},
    },
    "required": ["context_check"],
}

class ContextMetric(BaseMetric):
    key = 'context' 

    def __init__(self, api_key, base_url, model, model_provider='openai'):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model
        self.model_provider = model_provider

    def evaluate(self, chat):
        try:
            system_message = context_prompt

            conversation = f"context:\n {chat.openai_prompt}\n " \
                           f"user-query:\n {chat.user_query}\n" \
                           f"bot-response:\n {chat.openai_response}\n"

            messages = [
                {"role": "user", "content": system_message},
                {"role": "user", "content": conversation},
            ]

            functions = [{"name": "context_schema", "parameters": context_schema}]
            function_call = {"name": "context_schema"}

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

            return parsed_response['context_check']
        except Exception as e:
            return f"Failed to evaluate ContextMetric::evaluate::{e}"

