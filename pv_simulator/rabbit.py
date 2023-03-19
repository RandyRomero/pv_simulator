import json
import logging
import typing as tp
from asyncio import AbstractEventLoop

from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

logger = logging.getLogger("pv_simulator.rabbit")


class RabbitClient:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection
        self._channel: AbstractChannel

    async def connect(self, login: str, password: str, host: str, port: int, loop: AbstractEventLoop) -> None:
        """
        Establishes connection and channel.

        For production code it is better to use connection pool and
        channel pool, but for such a tiny app there is not point in doing that
        """

        self._connection = await connect_robust(
            login=login, password=password, host=host, port=port, loop=loop, timeout=5
        )
        self._channel = await self._connection.channel()

    async def consume(
        self, exchange_name: str, queue_name: str, routing_key: str, callback: tp.Callable[..., tp.Awaitable[tp.Any]]
    ) -> None:
        """Consumes rabbit messages."""
        await self._channel.set_qos(prefetch_count=10)

        exchange = await self._channel.declare_exchange(exchange_name, type=ExchangeType.DIRECT, durable=True)
        queue = await self._channel.declare_queue(queue_name, durable=True)

        await queue.bind(exchange=exchange, routing_key=routing_key)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(ignore_processed=True, reject_on_redelivered=True) as msg:
                    try:
                        message_body = json.loads(message.body)
                    except json.decoder.JSONDecodeError as ex:
                        await msg.nack(requeue=False)
                        logger.error("Json decode error: %s", ex)
                        continue

                    try:
                        await callback(message_body)
                        await msg.ack()
                    except Exception as err:
                        logger.exception(err)
                        await msg.nack(requeue=False)
