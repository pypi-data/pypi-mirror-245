from sona.settings import settings

from .base import StreamMiddlewareBase

middlewares = [
    StreamMiddlewareBase.load_class(kls)()
    for kls in settings.SONA_STREAM_MIDDLEWARE_CLASSES
]
