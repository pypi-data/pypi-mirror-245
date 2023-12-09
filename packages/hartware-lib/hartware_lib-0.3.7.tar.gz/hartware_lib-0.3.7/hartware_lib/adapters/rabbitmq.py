from __future__ import annotations

import asyncio
from logging import getLogger
from typing import Any, List

from aio_pika import DeliveryMode, ExchangeType, Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage

from hartware_lib.serializers import deserialize as default_deserializer
from hartware_lib.serializers import serialize as default_serializer
from hartware_lib.settings import RabbitMQSettings

logger = getLogger(__name__)


class RabbitMQAdapter:
    def __init__(
        self,
        settings: RabbitMQSettings,
        serializer,
        deserializer,
        object_class: Any = object,
    ):
        self.settings = settings
        self.serializer = serializer
        self.deserializer = deserializer
        self.object_class = object_class

    async def get_connection(self):
        return await connect_robust(
            f"amqp://{self.settings.username}:{self.settings.password}@{self.settings.host}:{self.settings.port}/"
        )

    def handle_message(self, callback):
        async def wrapper(message: AbstractIncomingMessage) -> None:
            async with message.process():
                obj = self.deserializer(message.body)

                return await callback(self, obj)

        return wrapper

    def encode_object(self, obj):
        if not isinstance(obj, self.object_class):
            raise Exception(f"Message must be of type `{self.object_class.__name__}`")

        return self.serializer(obj)

    def to_message(self, obj):
        message_body = self.encode_object(obj)

        return Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)

    async def run_message_on_default_exchange(self, connection, obj, routing_key):
        channel = await connection.channel()

        await channel.default_exchange.publish(
            self.to_message(obj), routing_key=routing_key
        )

    async def run_consumer_on_default_exchange(self, connection, callback, routing_key):
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(routing_key, durable=True)

        await queue.consume(self.handle_message(callback))

        await asyncio.Future()

    async def run_message_on_fanout_exchange(
        self, connection, obj, exchange_name, routing_key="none"
    ):
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchange_name, ExchangeType.FANOUT)

        await exchange.publish(self.to_message(obj), routing_key=routing_key)

    async def run_consumer_on_fanout_exchange(
        self, connection, callback, exchange_name
    ):
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(exchange_name, ExchangeType.FANOUT)
        queue = await channel.declare_queue(exclusive=True)

        await queue.bind(exchange)
        await queue.consume(self.handle_message(callback))

        await asyncio.Future()

    async def run_message_on_topic_exchange(
        self, connection, obj, exchange_name, routing_key
    ):
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchange_name, ExchangeType.TOPIC)

        await exchange.publish(self.to_message(obj), routing_key=routing_key)

    async def run_consumer_on_topic_exchange(
        self, connection, callback, exchange_name: str, binding_keys: List[str]
    ):
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(exchange_name, ExchangeType.TOPIC)
        queue = await channel.declare_queue("", durable=True)

        for binding_key in binding_keys:
            await queue.bind(exchange, routing_key=binding_key)

        await queue.consume(self.handle_message(callback))

        await asyncio.Future()

    def get_flavor_adapter(self, flavor: str, *args, **kwargs) -> RabbitMQFlavor:
        kwargs.update(self.__dict__)

        if flavor == "default":
            return RabbitMQDefaultExchangeAdapter(*args, **kwargs)
        elif flavor == "fanout":
            return RabbitMQFanoutExchangeAdapter(*args, **kwargs)
        elif flavor == "topic":
            return RabbitMQTopicExchangeAdapter(*args, **kwargs)
        else:
            raise Exception(f"No flavor '{flavor}'")


class RabbitMQFlavor(RabbitMQAdapter):
    def __init__(self, *args, **kwargs):
        super(RabbitMQFlavor, self).__init__(*args, **kwargs)

        self._connection = None

    async def ensure_connection(self):
        if self._connection is None:
            self._connection = await self.get_connection()

    @property
    async def connected(self):
        await self.ensure_connection()

        return self._connection

    def _publish(self, *args, **kwargs):
        raise NotImplementedError

    def _consume(self, *args, **kwargs):
        raise NotImplementedError

    async def publish(self, *args, **kwargs):
        await self.ensure_connection()

        await self._publish(self._connection, *args, **kwargs)

    async def consume(self, *args, **kwargs):
        await self.ensure_connection()

        await self._consume(self._connection, *args, **kwargs)


class RabbitMQDefaultExchangeAdapter(RabbitMQFlavor):
    def __init__(self, *args, routing_key: str, **kwargs):
        super(RabbitMQDefaultExchangeAdapter, self).__init__(*args, **kwargs)

        self.routing_key = routing_key

    async def _publish(self, connection, obj):
        await self.run_message_on_default_exchange(connection, obj, self.routing_key)

    async def _consume(self, connection, callback):
        return await self.run_consumer_on_default_exchange(
            connection, callback, self.routing_key
        )


class RabbitMQFanoutExchangeAdapter(RabbitMQFlavor):
    def __init__(self, *args, exchange_name: str, **kwargs):
        super(RabbitMQFanoutExchangeAdapter, self).__init__(*args, **kwargs)

        self.exchange_name = exchange_name

    async def _publish(self, connection, obj):
        await self.run_message_on_fanout_exchange(connection, obj, self.exchange_name)

    async def _consume(self, connection, callback):
        return await self.run_consumer_on_fanout_exchange(
            connection, callback, self.exchange_name
        )


class RabbitMQTopicExchangeAdapter(RabbitMQFlavor):
    def __init__(self, *args, exchange_name: str, **kwargs):
        super(RabbitMQTopicExchangeAdapter, self).__init__(*args, **kwargs)

        self.exchange_name = exchange_name

    async def _publish(self, connection, obj, routing_key):
        await self.run_message_on_topic_exchange(
            connection, obj, self.exchange_name, routing_key
        )

    async def _consume(self, connection, callback, binding_keys):
        return await self.run_consumer_on_topic_exchange(
            connection, callback, self.exchange_name, binding_keys
        )


def rabbitmq_adapter_factory(
    settings: RabbitMQSettings,
    serializer=default_serializer,
    deserializer=default_deserializer,
    object_class=dict,
):
    return RabbitMQAdapter(settings, serializer, deserializer, object_class)
