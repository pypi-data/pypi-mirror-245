import abc

from sona.core.stream.messages.context import StreamContext
from sona.utils.common import import_class


class StreamMiddlewareBase:
    def on_context(self, on_context):
        def decorator(ctx: StreamContext):
            return self.wrapper_on_context(ctx, on_context)

        return decorator

    def on_close(self, on_close):
        def decorator():
            return self.wrapper_on_context(on_close)

        return decorator

    @abc.abstractmethod
    def wrapper_on_context(self, ctx: StreamContext, on_context):
        return NotImplemented

    @classmethod
    def load_class(cls, import_str):
        _cls = import_class(import_str)
        if _cls not in cls.__subclasses__():
            raise Exception(f"Unknown middleware class: {import_str}")
        return _cls
