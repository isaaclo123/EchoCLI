import socket
import enum
import logging

_LOGGER = logging.getLogger()

class LEDOption(enum.Enum):
    MICS_OFF_ON = "mics-off_on"
    MICS_OFF_START = "mics-off_start"
    MICS_OFF_END = "mics-off_end"
    ERROR = "error"
    OFF = "off"
    SOLID_BLUE = "solid_blue"
    SOLID_CYAN = "solid_cyan"
    SOLID_GREEN = "solid_green"
    SOLID_ORANGE = "solid_orange"
    SOLID_RED = "solid_red"
    SOLID_WHITE = "solid_white"
    ZZZ_DISCO = "zzz_disco"
    ZZZ_RAINBOW = "zzz_rainbow"
    ZZZ_TURBO_BOOST = "zzz_turbo-boost"

class EchoLEDNetworkClient():
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.prev_led_option = ""
        _LOGGER.debug("echo network socket created")

    def connect(self):
        _LOGGER.debug("Connecting to echo network socket")
        self.socket.connect((self.host, self.port))

    def close(self):
        self.prev_led_option = ""
        _LOGGER.debug("Closing network socket")
        self.socket.close()

    def set(self, led_option: LEDOption) -> bool:
        if led_option.value == self.prev_led_option:
            # if you are sending the same LED option; don't send
            _LOGGER.debug("LED option: '%s' already set; not sending", led_option.value)
            return True

        self.socket.sendall(str.encode(f"${led_option.value}\n"))
        result = self.socket.recv(64)

        if result == b"0\n":
            # success
            self.prev_led_option = led_option.value
            _LOGGER.debug("LED option: '%s' set successfully", led_option.value)
            return True
        _LOGGER.debug("LED option: '%s' failed to be set", led_option.value)
        return False


if __name__ == "__main__":
    HOST="http://192.168.1.91"  # Replace with the local IP of the echo dot
    PORT = 8000 # The port used by the echo dot
    led_client = EchoLEDNetworkClient(HOST, PORT)
    led_client.connect()

    print("test1", led_client.set(LEDOption.MICS_OFF_END))
    print("test1.5", led_client.set(LEDOption.MICS_OFF_END))
    print("test2", led_client.set(LEDOption.MICS_OFF_START))

    led_client.close()
