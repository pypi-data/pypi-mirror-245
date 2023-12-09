from .strategy import openai_strategy, azure_strategy

class ModelProvider:

    def get_strategy(self, model_provider=None, api_key=None, base_url=None):
        if model_provider is None or model_provider == "openai":
            return openai_strategy.OpenAIStrategy(api_key=api_key, base_url=base_url)
        if model_provider == "azure":
            return azure_strategy.AzureStrategy(api_key=api_key, base_url=base_url)

    def chat_completion(self,
                        api_key,
                        base_url,
                        model_provider,
                        messages,
                        model=None,
                        **completion_api_params):

        strategy = self.get_strategy(model_provider=model_provider, api_key=api_key, base_url=base_url)
        if strategy is None:
            raise "Model type not found"
        try:
            return strategy.chat_completion(model=model,
                                            messages=messages,
                                            **completion_api_params)
        except Exception as e:
            raise e
