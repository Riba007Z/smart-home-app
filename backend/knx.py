from xknx import XKNX
from xknx.io import ConnectionConfig, ConnectionType

from websocket_manager import broadcast
import asyncio


xknx = XKNX(
    connection_config=ConnectionConfig(
        connection_type=ConnectionType.TUNNELING,
        gateway_ip="192.168.64.118",
        gateway_port=3671,
    )
)


states = {}


def telegram_received(telegram):

    print(
        "TELEGRAM:",
        telegram.destination_address,
        telegram.payload.value
    )

    if telegram.payload.value is not None:

        address = str(telegram.destination_address)
        value = bool(telegram.payload.value.value)

        states[address] = value

        asyncio.create_task(
            broadcast({
                "address": address,
                "value": value
            })
        )


async def start_knx():

    xknx.telegram_queue.register_telegram_received_cb(
        telegram_received
    )

    await xknx.start()


    print("KNX connected")


async def stop_knx():

    await xknx.stop()

    print("KNX stopped")


def get_states():
    return states