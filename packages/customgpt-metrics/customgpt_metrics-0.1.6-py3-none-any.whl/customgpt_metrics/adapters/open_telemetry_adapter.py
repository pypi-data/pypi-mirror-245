from .types.log_entry import LogEntry

class OpenTelemetryAdapter:
    def adapt_log_entry(self, log_entry):
        adapted_entry = LogEntry(**log_entry)
        return adapted_entry
