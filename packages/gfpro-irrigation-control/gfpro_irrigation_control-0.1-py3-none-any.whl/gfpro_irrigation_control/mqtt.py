import logging
import threading
from typing import Optional, Union

import paho.mqtt.client as mqtt

from gfpro_irrigation_control.valve import GFProBluetoothValve

logger = logging.getLogger(__name__)


class MQTTGFProBluetoothValveController:

    def __init__(
            self,
            valve: Union[GFProBluetoothValve, str],
            *,
            name: Optional[str] = None,
            mqtt_host: str = "localhost",
            mqtt_port: int = 1883,
            mqtt_keep_alive: int = 60,
            valve_state_interval: int = 10,
            diagnostics_interval: int = 3600,
    ):

        # Set up valve
        if isinstance(valve, str):
            self.valve = GFProBluetoothValve(valve)
        else:
            self.valve = valve

        self.valve.on_connect = self._valve_connected
        self.valve.on_disconnect = self._valve_disconnected

        # Read config
        if name is None:
            self.name = self.valve.mac
        else:
            self.name = name

        self.valve_state_interval = valve_state_interval
        self.diagnostics_interval = diagnostics_interval

        self.base_topic = f"gfpro-irrigation-valve/{self.name}/{{topic}}"
        self.status_topic = self.base_topic.format(topic='connection_status')

        self.valve_state_topic = self.base_topic.format(topic='valve_state')
        self.valve_target_state_topic = self.base_topic.format(topic='target_valve_state')

        # create client
        self.client = mqtt.Client()

        self.client.on_connect = self._client_connected
        self.client.on_disconnect = self._client_disconnected
        self.client.on_message = self._message_received
        self.client.will_set(self.status_topic, 0, retain=True)
        self.client.connect_async(mqtt_host, mqtt_port, mqtt_keep_alive)

        self.transmission_stop_event = threading.Event()
        self.transmission_stop_event.set()

        self.stop_event = threading.Event()
        self.stop_event.set()

    def publish_valve_state(self):
        logger.debug("Publishing valve state.")

        self.client.publish(
            self.valve_state_topic,
            int(self.valve.is_open()),
            retain=True,
        )

    def publish_diagnostics(self):
        logger.debug("Publishing battery state.")

        diagnostics = self.valve.read_diagnostics()
        self.client.publish(
            self.base_topic.format(topic="battery_level"),
            int(diagnostics.battery_level),
            retain=True,
        )
        self.client.publish(
            self.base_topic.format(topic="battery_voltage"),
            diagnostics.battery_voltage,
            retain=True,
        )

    def _execute_periodically(self, function, description, interval):
        logger.info(f"Starting the periodical transmission of {description} (interval: {interval} seconds).")

        function()
        while not self.stop_event.wait(interval):
            function()

    def start_periodic_transmission(self):
        if self.stop_event.is_set():
            self.stop_event.clear()

            threading.Thread(
                target=self._execute_periodically,
                args=(self.publish_valve_state, "valve state", self.valve_state_interval),
            ).start()
            threading.Thread(
                target=self._execute_periodically,
                args=(self.publish_diagnostics, "battery state", self.diagnostics_interval),
            ).start()

    def stop_periodic_transmission(self):
        if not self.stop_event.is_set():
            logger.info(f"Stopping periodical signal transmission for valve {self.name}.")
            self.stop_event.set()

    def _valve_connected(self):
        logger.info("Connected to valve.")
        self.client.publish(self.status_topic, 1, retain=True)
        self.client.subscribe(self.valve_target_state_topic)
        self.start_periodic_transmission()

    def _valve_disconnected(self, error=None):
        logger.info("Disconnected from valve.")
        self.client.publish(self.status_topic, 0, retain=True)
        self.stop_periodic_transmission()

    def _client_connected(self, _, userdata, flags, rc):
        logger.info("Connected to MQTT broker.")
        threading.Thread(target=self.valve.autoconnect).start()

    def _client_disconnected(self, _, userdata, rc):
        logger.info("Disconnected from MQTT broker.")
        self.stop_periodic_transmission()
        threading.Thread(target=self.valve.disconnect).start()

    def _message_received(self, _, userdata, msg):
        if msg.payload == b'1':
            logger.info("Opening valve.")
            self.valve.open_valve()
            self.publish_valve_state()

        elif msg.payload == b'0':
            logger.info("Closing valve.")
            self.valve.close_valve()
            self.publish_valve_state()

        else:
            logger.warning("Received invalid target state.")

    def start(self):
        logger.info("Starting MQTT GFPro bluetooth valve controller.")
        logger.info("Connecting to MQTT broker.")

        try:
            self.client.loop_forever(retry_first_connection=True)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.client.publish(self.status_topic, 0, retain=True)
        logger.info("Stopping MQTT GFPro bluetooth valve controller.")
        logger.info("Disconnecting from MQTT broker.")
        self.client.disconnect()
