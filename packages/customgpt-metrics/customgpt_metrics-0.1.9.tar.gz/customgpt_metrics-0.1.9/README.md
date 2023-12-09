# CustomGPT Metrics SDK

**CustomGPT Metrics** is a Python SDK designed to analyze and evaluate chatbot interactions using various metrics. This SDK seamlessly integrates with the CustomGPT platform, offering a straightforward way to assess chatbot performance.

## Installation

To install the CustomGPT Metrics SDK, use the following `pip` command:

```bash
pip install customgpt_metrics
```

## Usage

1. First basic way to use the metrics sdk is to pass a dict and the sdk will out the metric using analyze_log method.

```python
from customgpt_metrics import CustomGPTMetrics

# Initialize the CustomGPTMetrics object
metrics = CustomGPTMetrics(api_key="your_api_key_here")

# Define a sample chat interaction
input_chat = {
    'user_query': 'Can I upload my PDF files to build the ChatGPT chatbot?',
    'openai_query': """Using only the following context, answer the questions.
    If context has no information about the question say sorry you can't answer as you don't have enough knowledge about that subject.
    You are a custom chatbot assistant called CustomGPT that answers questions based on the given context.
    Be as helpful as possible.
    ...
    --END OF CONTEXT--""",
    'openai_response': 'Yes, you can upload your PDF files to build the ChatGPT chatbot. The platform supports uploading documents in 1400+ formats, including PDFs, Microsoft Office docs, Google docs, and audio files. You can simply go to your CustomGPT dashboard and upload the documents to build your custom chatbots in minutes.'
}

# Analyze the chat interaction
output = metrics.analyze_log(input_chat)

# Access individual metric values
print(f"Context Check: {output.context_check}")
print(f"Emotion Check: {output.emotion_check}")
print(f"Intent Check: {output.intent_check}")
print(f"Language Check: {output.language_check}")
```
2. The other way to use inject logs to the sdk is by using MySQL Database url passed to analyze_logs and allows streaming to get output for each metric.

```
from customgpt_metrics import CustomGPTMetrics

metrics = CustomGPTMetrics(api_key="your_api_key_here")
metric_outputs = metrics.stream_analyze_logs("mysql://root:password@localhost/customgpt", limit=10, metrics=['emotion', 'context', 'language', 'intent'])
for output in metric_outputs:
    print(output)
```
3. The other way to use inject logs to the sdk is by using MySQL Database url passed to analyze_logs and allows to get output as list.

```
from customgpt_metrics import CustomGPTMetrics

metrics = CustomGPTMetrics(api_key="your_api_key_here")
metric_outputs = metrics.analyze_logs("mysql://root:password@localhost/customgpt", limit=10, metrics=['emotion', 'context', 'language', 'intent'])

for output in metric_outputs:
    print(output)
```

# Easy Metric Addition Capability

To add more metrics to the output all you need to do is add another python file to metrics directory. It should be subclass of BaseMetric
```
class BaseMetric:
    key = None
    
    def __init__(self, api_key, base_url, model_provider='openai'):
        pass
    def evaluate(self, log_entry):
        # Add logic to evaluate the metric based on the adapted log entry
        pass
```

Make sure to replace `"your_api_key_here"` with your actual OpenAI API key.

The SDK allows for easy analysis of various metrics and provides flexibility to customize metrics based on your requirements. The output is a parsed `Metric` object containing the evaluated metric values.

Explore the additional features and metrics provided by the CustomGPT Metrics SDK to tailor the analysis to your specific use case.
