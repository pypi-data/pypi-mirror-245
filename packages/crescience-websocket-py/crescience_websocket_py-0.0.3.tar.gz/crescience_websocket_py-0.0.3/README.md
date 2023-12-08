# Crescience Websocket Client

Websocket client for Crescience devices written in python.

## Requirements

- python>=3.7
- pip

## Installation

You can install the client using `pip`:

```bash
pip install crescience-websocket-py
```

## Usage

The client provides two different usage cases:

### Callback

```python
from crescience_websocket_py import WebsocketClient, Message, ConnectionMessageType


def callback(msg_type: ConnectionMessageType, msg: Message | None, error:ConnectionErrorReason | None) -> None:
    if msg_type==ConnectionMessageType.TEXT:
        print(f"Received message: {str(msg)}")
    elif msg_type==ConnectionMessageType.OPEN:
        print("Connection opened")
    elif msg_type==ConnectionMessageType.ERROR:
        print(f"Connection error: {error}")
    elif msg_type==ConnectionMessageType.CLOSE:
        print("Connection closed")

client=WebsocketClient(
    host="<IP_OR_DOMAIN>",
    port=81,
    verify_ssl=False,
    callback=callback
)
```

### Class inheritance

```python
from crescience_websocket_py import WebsocketClient, Message, ConnectionMessageType


class MyCrescienceClient(WebsocketClient):
    def __init__(self, host:str) -> None:
        super().__init__(host=host, port=81, verify_ssl=False)

    async def received(self, msg: Message) -> None:
        print(f"Received message: {str(msg)}")

    async def on_open(self) -> None:
        print("Connection opened")

    async def on_close(self) -> None:
        print("Connection closed")

    async def on_error(self, error:ConnectionMessageType) -> None:
        print(f"Connection error: {error}")

client=MyCrescienceClient("<IP_OR_DOMAIN>")
```

## Check for firmware-updates

You can check if firmware updates are available using the following command:

```python
from crescience_websocket_py import get_latest_version

latest_version = get_latest_version(device_type="crescontrol")

print(latest_version["version"])
```
