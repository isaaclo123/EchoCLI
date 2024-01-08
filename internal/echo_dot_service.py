#!/usr/bin/env python3
"""Controls the LEDs on the Echo Dot 2; built for the Wyoming Satellite protocol."""
import argparse
import asyncio
import logging
import time
from functools import partial
from examples.echo_led_client import EchoLEDNetworkClient, LEDOption

from wyoming.asr import Transcript
from wyoming.event import Event
from wyoming.satellite import RunSatellite, StreamingStarted, StreamingStopped
from wyoming.server import AsyncEventHandler, AsyncServer
from wyoming.vad import VoiceStarted
from wyoming.wake import Detection

_LOGGER = logging.getLogger()

async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", required=True, help="unix:// or tcp://")
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")

    parser.add_argument("--echo_host", required=True, help="echo dot 2 led server ip")
    parser.add_argument("--echo_port", required=True, help="echo dot 2 led server port")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    _LOGGER.debug(args)

    _LOGGER.info("Ready")

    # setup echo led client
    led_client = EchoLEDNetworkClient(args.echo_host, args.echo_port)

    # Start server
    server = AsyncServer.from_uri(args.uri)

    try:
        await server.run(partial(LEDsEventHandler, args))
    except KeyboardInterrupt:
        pass
    finally:
        led_client.close()



# -----------------------------------------------------------------------------


class LEDsEventHandler(AsyncEventHandler):
    """Event handler for clients."""

    def __init__(
        self,
        cli_args: argparse.Namespace,
        led_client: EchoLEDNetworkClient,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.cli_args = cli_args
        self.led_client = led_client
        self.client_id = str(time.monotonic_ns())

        led_client.connect()
        _LOGGER.debug("Client connected: %s", self.client_id)

    async def handle_event(self, event: Event) -> bool:
        _LOGGER.debug(event)

        if StreamingStarted.is_type(event.type):
            self.led_client.set(LEDOption.SOLID_ORANGE)
        elif Detection.is_type(event.type):
            self.led_client.set(LEDOption.SOLID_BLUE)
            await asyncio.sleep(1.0)  # show for 1 sec
            self.led_client.set(LEDOption.OFF)
        elif VoiceStarted.is_type(event.type):
            self.led_client.set(LEDOption.SOLID_ORANGE)
        elif Transcript.is_type(event.type):
            self.led_client.set(LEDOption.SOLID_GREEN)
            await asyncio.sleep(1.0)  # show for 1 sec
            self.led_client.set(LEDOption.OFF)
        elif StreamingStopped.is_type(event.type):
            self.led_client.set(LEDOption.OFF)
        elif RunSatellite.is_type(event.type):
            self.led_client.set(LEDOption.OFF)

        return True


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
