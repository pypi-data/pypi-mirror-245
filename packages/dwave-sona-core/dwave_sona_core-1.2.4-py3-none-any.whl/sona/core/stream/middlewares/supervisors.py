import boto3
from loguru import logger
from sona.core.messages.context import Context
from sona.core.stream.messages.context import EvtType, StreamContext
from sona.settings import settings

from .base import StreamMiddlewareBase

try:
    from confluent_kafka import Producer
except ImportError:
    Producer = None

EMIT_INTERVAL_SEC = settings.SONA_STREAM_MIDDLEWARE_SUPERVISOR_EMIT_INTERVAL_SEC
TOPIC_LIST = settings.SONA_STREAM_MIDDLEWARE_SUPERVISOR_TOPIC_LIST
KAFKA_SETTING = settings.SONA_STREAM_MIDDLEWARE_SUPERVISOR_KAFKA_SETTING
SQS_SETTING = settings.SONA_STREAM_MIDDLEWARE_SUPERVISOR_SQS_SETTING


class KafkaStreamSupervisor(StreamMiddlewareBase):
    def __init__(
        self, configs=KAFKA_SETTING, interval=EMIT_INTERVAL_SEC, topics=TOPIC_LIST
    ):
        self.duration = 0
        self.topics = topics
        self.init_interval = interval
        self.interval = self.init_interval
        if Producer:
            self.producer = Producer(configs)
        else:
            logger.warning(
                "Missing SONA_MIDDLEWARE_SUPERVISOR_KAFKA_SETTING, KafkaSupervisor will be ignored."
            )
            self.producer = None

    def wrapper_on_context(self, ctx: StreamContext, on_context):
        on_context(ctx)

        if ctx.event_type != EvtType.AV_AUDIO.value:
            return

        duration = ctx.payload.samples / ctx.payload.rate
        self.duration += duration
        self.interval -= duration
        if self.interval < 0:
            self.interval = self.init_interval
            for topic in self.topics:
                Context(headers=ctx.headers, jobs=[], states=[], results={})
                # self._emit(topic, ctx.)

    def _emit(self, topic, message):
        try:
            if self.producer:
                self.producer.poll(0)
                self.producer.produce(
                    topic, message.encode("utf-8"), callback=self.__delivery_report
                )
                self.producer.flush()
        except Exception as e:
            logger.warning(f"Supervisor emit error occur {e}, ignore message {message}")

    def __delivery_report(self, err, msg):
        if err:
            raise Exception(msg.error())


class SQSStreamSupervisor(StreamMiddlewareBase):
    def __init__(self, setting=SQS_SETTING, interval=EMIT_INTERVAL_SEC):
        self.duration = 0
        self.init_interval = interval
        self.interval = self.init_interval
        self.sqs = boto3.resource("sqs", **setting)

    def wrapper_func(self, ctx: StreamContext, on_context):
        on_context(ctx)

        if ctx.event_type != EvtType.AV_AUDIO.value:
            return

        duration = ctx.payload.samples / ctx.payload.rate
        self.duration += duration
        self.interval -= duration
        if self.interval < 0:
            self.interval = self.init_interval

    def _emit(self, topic, message):
        try:
            queue = self.sqs.get_queue_by_name(QueueName=topic)
            queue.send_message(MessageBody=message)
        except Exception as e:
            logger.warning(f"Supervisor emit error occur {e}, ignore message {message}")
