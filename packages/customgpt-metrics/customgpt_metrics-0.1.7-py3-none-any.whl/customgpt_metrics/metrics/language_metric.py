from .base_metric import BaseMetric
from .model_provider import model_provider
import json

language_schema = {
    "type": "object",
    "properties": {
      "language_type": {"type": "string",
                          "description": "The ISO code of the language that the user used in user-query. Output the most similar language.",
                          "enum": [
                            "aa", "ab", "af", "ak", "sq", "am", "ar", "an", "hy", "as", "av", "ae", "ay", "az", "bm", "ba", "eu",
                            "be", "bn", "bh", "bi", "bs", "br", "bg", "my", "ca", "km", "ch", "ce", "ny", "zh", "cv", "kw", "co",
                            "cr", "hr", "cs", "da", "dv", "nl", "dz", "en", "eo", "et", "ee", "fo", "fj", "fi", "fr", "ff", "gl",
                            "ka", "de", "el", "gn", "gu", "ht", "ha", "he", "hz", "hi", "ho", "hu", "ia", "id", "ie", "ga", "ig",
                            "ik", "io", "is", "it", "iu", "ja", "jv", "kl", "kn", "kr", "ks", "kk", "km", "ki", "rw", "ky", "kv",
                            "kg", "ko", "ku", "kj", "la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv", "gv", "mk", "mg", "ms",
                            "ml", "mt", "mi", "mr", "mh", "mn", "na", "nv", "nb", "nd", "ne", "ng", "nn", "no", "ii", "nr", "oc",
                            "oj", "cu", "om", "or", "os", "pa", "pi", "fa", "pl", "ps", "pt", "qu", "ro", "rm", "rn", "ru", "sa",
                            "sc", "sd", "se", "sm", "sg", "sr", "gd", "sn", "si", "sk", "sl", "so", "st", "es", "su", "sw", "ss",
                            "sv", "ta", "te", "tg", "th", "ti", "bo", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ty", "ug",
                            "uk", "ur", "uz", "ve", "vi", "vo", "wa", "cy", "wo", "fy", "xh", "yi", "yo", "za", "zu"
                            ]
                        }
    },
    "required": ["language_type"]
}

language_prompt = "You are an expert AI language interpreter. Please analyze the message below delimited by $$$ " \
                  "and output the detected language used to write the message. STRICTLY Output ONLY the ISO code of the language."

class LanguageMetric(BaseMetric):
    key = 'language'

    def __init__(self, api_key, base_url, model, model_provider='openai'):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model
        self.model_provider = model_provider
    
    def evaluate(self, chat):
        try:
            system_message = language_prompt
            user_query = f"User Query\n $$$  {chat.user_query} $$$"

            messages = [
                {"role": "user", "content": system_message},
                {"role": "user", "content": user_query}
            ]

            functions = [{"name": "language_schema", "parameters": language_schema}]
            function_call = {"name": "language_schema"}

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

            return parsed_response['language_type']

        except Exception as e:
            return f"Failed to evaluate LanguageMetric::evaluate::{e}"