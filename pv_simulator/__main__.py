import asyncio
import logging
import random
import typing as tp
from asyncio import AbstractEventLoop

from pv_simulator.rabbit import RabbitClient
from pv_simulator.serializers.rabbit_messages import MeterValue
from pv_simulator.settings import settings

output_queue: asyncio.Queue = asyncio.Queue()

EXCHANGE_NAME = "METER"
ROUTING_KEY = "meter_value"
QUEUE_NAME = "meter_values_queue"

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger("pv_simulator")

# suppress loggers from external libraries
logging.getLogger("aiormq").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# A dedicated logger to write meter value, pv simulator value and their sum on the disk.
# A good idea could be to write these values not with logger, but with csv writer to a csv file instead
file_logger = logging.getLogger("pv_simulator.file_logger")
file_handler = logging.FileHandler("./pv_simulator/logs/output.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(lineno)s:%(message)s"))
file_handler.setLevel(logging.DEBUG)
file_logger.addHandler(file_handler)


async def output() -> None:
    """Output the meter value, pv simulator value and their sum."""

    while True:
        meter_value = await output_queue.get()
        pv_value = await get_pv_value()

        file_logger.info(
            "Meter value: %d; pv_simulator_value: %d; sum: %d", meter_value, pv_value, meter_value + pv_value
        )


async def process_message(msg: tp.Dict[str, tp.Any]) -> None:
    """
    Process rabbit messages.

    - checks that the message has the correct schema.
    - puts the message to the queue to be processed further
    """

    logger.debug("Got a new msg: %s", str(msg))
    meter_value = MeterValue(**msg).value
    await output_queue.put(meter_value)


async def get_pv_value() -> int:
    """Example of implementation."""
    new_pv_value = random.randint(0, 3500)
    logger.info("New pv value: %d", new_pv_value)
    return new_pv_value


async def main(event_loop: AbstractEventLoop) -> None:
    """
    Sets up and starts the app.

    - sets up the rabbit client
    - starts consumer messages
    - start writing the information to a disk
    """
    rabbitmq = RabbitClient()
    await rabbitmq.connect(
        settings.RABBIT_LOGIN,
        settings.RABBIT_PASSWORD,
        settings.RABBIT_HOST,
        settings.RABBIT_PORT,
        event_loop,
    )

    await asyncio.gather(rabbitmq.consume(EXCHANGE_NAME, QUEUE_NAME, ROUTING_KEY, process_message), output())


if __name__ == "__main__":
    logger.info("Initializing...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
