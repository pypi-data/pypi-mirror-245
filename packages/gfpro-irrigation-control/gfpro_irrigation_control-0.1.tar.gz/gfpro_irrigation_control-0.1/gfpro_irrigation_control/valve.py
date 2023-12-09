import logging
import struct
import threading
import time
from dataclasses import dataclass
from itertools import count
from typing import Any, Callable, Optional

from bluepy.btle import Peripheral

logger = logging.getLogger(__name__)


@dataclass
class Diagnostics:
    battery_voltage: int

    @property
    def battery_level(self):
        return 100 * min(min((self.battery_voltage - 3100) / 750, 0), 1)


class GFProBluetoothValve:
    DEFAULT_PASSWORD = '123456'  # noqa: S105

    PASSWORD_CHARACTERISTIC = 0x48
    TEMPERATURE_CHARACTERISTIC = 0x3b
    VALVE_SETTER_CHARACTERISTIC = 0x13
    VALVE_GETTER_CHARACTERISTIC = 0x15
    BATTERY_CHARACTERISTIC = 0x39

    def __init__(self, mac, password=DEFAULT_PASSWORD):
        self.mac = mac
        self.device = None
        self.password = password

        self.lock = threading.Lock()

    def on_connect(self):
        pass

    def on_disconnect(self, error=None):
        pass

    def is_connected(self):
        try:
            return self.device is not None and self.device.getState() == 'conn'
        except Exception:
            return False

    def connect(self):
        logger.info(f"Connecting to G.F.Pro Eco Watering bluetooth valve at {self.mac}")

        if not self.is_connected():
            self.device = Peripheral(self.mac)

        password_bytes = self.password.encode()

        while True:
            logging.debug("Authenticating...")
            self.device.writeCharacteristic(self.PASSWORD_CHARACTERISTIC, password_bytes, withResponse=True)

            if self.device.readCharacteristic(self.PASSWORD_CHARACTERISTIC) == password_bytes:
                logging.info("Connected.")
                self.on_connect()
                return
            else:
                logging.debug("Authentication did not work. Trying again...")
                time.sleep(0.5)

    def autoconnect(self, attempts: Optional[int] = None, delay: int = 5, post_connect_delay: float = 0.5):
        for attempt in count() if attempts is None else range(attempts):
            try:
                self.connect()
                time.sleep(post_connect_delay)
                return
            except Exception:
                logger.info(f"Connecting attempt #{attempt + 1} failed. Waiting {delay} seconds before trying again.")
                time.sleep(delay)

    def disconnect(self):
        if self.is_connected():
            self.device.disconnect()
        self.device = None
        logging.info("Disconnected.")
        self.on_disconnect()

    def _execute_safely(self, func: Callable[[Peripheral], Any]):
        with self.lock:
            while True:
                try:
                    return func(self.device)
                except Exception as e:
                    logging.info(f"Unexpected error: {e}.")
                    self.disconnect()
                    logging.info("Trying to reconnect.")
                    self.autoconnect()

    def read_temperature(self):
        data = self._execute_safely(lambda device: device.readCharacteristic(self.TEMPERATURE_CHARACTERISTIC))
        return struct.unpack('H', data)[0]

    def is_open(self):
        data = self._execute_safely(lambda device: device.readCharacteristic(self.VALVE_GETTER_CHARACTERISTIC))
        return data == b'\x01'

    def toggle_valve(self):
        logger.info("Toggling valve")
        self._execute_safely(
            lambda device: device.writeCharacteristic(self.VALVE_SETTER_CHARACTERISTIC, b'\x00', withResponse=True),
        )
        self._execute_safely(
            lambda device: device.writeCharacteristic(self.VALVE_SETTER_CHARACTERISTIC, b'\x01', withResponse=True),
        )

    def open_valve(self):
        if not self.is_open():
            self.toggle_valve()

    def close_valve(self):
        if self.is_open():
            self.toggle_valve()

    def read_diagnostics(self) -> Diagnostics:
        data = self._execute_safely(lambda device: device.readCharacteristic(self.BATTERY_CHARACTERISTIC))
        voltage = struct.unpack('H', data)[0]
        return Diagnostics(voltage)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
