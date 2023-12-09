from .types.metric import Metric

class MetricAdapter:
    @classmethod
    def parse_metric_output(self, output):
        metrics = {}
        for key, value in output.items():
            metrics[key] = output.get(key, None)
        return Metric(**metrics)
