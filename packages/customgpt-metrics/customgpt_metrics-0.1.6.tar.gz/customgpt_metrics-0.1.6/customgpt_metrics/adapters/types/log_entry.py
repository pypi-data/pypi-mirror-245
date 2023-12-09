class LogEntry:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attributes = ', '.join(f'{key}="{getattr(self, key)}"' for key in vars(self))
        return f'LogEntry({attributes})'

