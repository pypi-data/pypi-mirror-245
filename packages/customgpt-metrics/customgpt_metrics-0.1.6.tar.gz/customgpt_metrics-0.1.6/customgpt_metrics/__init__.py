from concurrent.futures import ThreadPoolExecutor, as_completed
from .adapters.open_telemetry_adapter import OpenTelemetryAdapter
from .adapters.sql_adapter import SQLAdapter
from .adapters.metric_adapter import MetricAdapter
from .metrics.base_metric import BaseMetric
from .metrics.utils import convert_to_class_name
import importlib
import time
import os

class CustomGPTMetrics:
    METRICS_FOLDER = 'metrics'

    def __init__(self, api_key=None, base_url='https://api.openai.com/v1', model_provider='openai', model=None, log_adapter=OpenTelemetryAdapter()):
        self.api_key = api_key
        self.log_adapter = log_adapter
        self.metrics = self.load_metrics(api_key, base_url, model_provider, model)

    def load_metrics(self, api_key, base_url, model_provider, model):
        metrics = {}
        metrics_folder_path = os.path.join(os.path.dirname(__file__), self.METRICS_FOLDER)
        for filename in os.listdir(metrics_folder_path):
            if filename.endswith('.py') and filename != '__init__.py':
                metric_name = filename[:-3]  # Remove '.py' extension
                metric_module = importlib.import_module(f"customgpt_metrics.{self.METRICS_FOLDER}.{metric_name}")
                metric_class = getattr(metric_module, convert_to_class_name(metric_name), None)
                if metric_class and issubclass(metric_class, BaseMetric) and metric_class != BaseMetric:
                    metrics[metric_class.key] = metric_class(api_key, base_url, model, model_provider)

        return metrics

    def analyze_log(self, chat):
        if self.api_key is None:
            raise ValueError("Metric Calculation require openai api_key to be set.")
        adapted_entry = self.log_adapter.adapt_log_entry(chat)
        metrics_result = {}

        with ThreadPoolExecutor() as executor:
            # Using executor.map to concurrently evaluate metrics
            metrics_values = executor.map(lambda metric: metric.evaluate(adapted_entry), self.metrics.values())

            for metric_name, metric_value in zip(self.metrics.keys(), metrics_values):
                metrics_result[metric_name] = metric_value

        metrics_result = MetricAdapter.parse_metric_output(metrics_result)
        return metrics_result

    def stream_analyze_logs(self, db_url, table='prompt_histories', query="SELECT * FROM %s LIMIT %s", limit=100):
        if self.api_key is None:
            raise ValueError("Metric Calculation require openai api_key to be set.")
        if db_url is None:
            raise ValueError("Database URL is required")
        try:
            sql_adapter = SQLAdapter()
            log_entries = sql_adapter.fetch_log_entries(db_url, table, query, limit)
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Using executor.map to concurrently evaluate metrics for each log entry
                results = []
                for log_entry in log_entries:
                    results.append(executor.submit(self.evaluate_metrics, log_entry))

                yield from self.process_results(results)
        except Exception as e:
            raise e

    def analyze_logs(self, db_url, table='prompt_histories', query="SELECT user_query, openai_response, openai_prompt FROM %s LIMIT %s", limit=10):
        if self.api_key is None:
            raise ValueError("Metric Calculation require openai api_key to be set.")
        if db_url is None:
            raise ValueError("Database URL is required")
        try:
            sql_adapter = SQLAdapter()
            log_entries = sql_adapter.fetch_log_entries(db_url, table, query, limit)

            output = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Using executor.map to concurrently evaluate metrics for each log entry
                results = []
                for log_entry in log_entries:
                    results.append(executor.submit(self.evaluate_metrics, log_entry))

                for future in as_completed(results):
                    result = future.result()
                    output.append(result)

            return output
        except Exception as e:
            raise e

    def evaluate_metrics(self, adapted_entry):
        metrics_result = {}
        with ThreadPoolExecutor() as executor:
            # Using executor.map to concurrently evaluate metrics
            metrics_values = executor.map(lambda metric: metric.evaluate(adapted_entry), self.metrics.values())

            for metric_name, metric_value in zip(self.metrics.keys(), metrics_values):
                metrics_result[metric_name] = metric_value
        metrics_result = MetricAdapter.parse_metric_output(metrics_result)
        return metrics_result

    @staticmethod
    def process_results(results):
        output = []
        for future in as_completed(results):
            result = future.result()
            yield result
