import argparse
import logging

from gfpro_irrigation_control.mqtt import MQTTGFProBluetoothValveController
from gfpro_irrigation_control.valve import GFProBluetoothValve


class ValveControlMQTTDaemon:

    @staticmethod
    def run():
        return ValveControlMQTTDaemon().parse_args()

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('mac', metavar='MAC', help="MAC address")
        self.parser.add_argument('--name', '-n', help="name to be used in the MQTT topic")
        self.parser.add_argument('--mqtt-host', '-m', help="MQTT broker host")
        self.parser.add_argument('--valve-state-interval', '-i', help="value state transmission interval")
        self.parser.add_argument('--diagnostics-interval', '-I', help="diagnostics transmission interval")
        self.parser.add_argument('--verbose', '-v', action='store_true', help="verbose mode")

    def parse_args(self, args=None):
        args = self.parser.parse_args(args)

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                            format='%(asctime)-15s %(levelname)-8s %(message)s')

        options = {}

        if args.name:
            options['name'] = args.name
        if args.mqtt_host:
            options['mqtt_host'] = args.mqtt_host
        if args.valve_state_interval:
            options['valve_state_interval'] = int(args.valve_state_interval)
        if args.diagnostics_interval:
            options['diagnostics_interval'] = int(args.diagnostics_interval)

        mqtt = MQTTGFProBluetoothValveController(valve=args.mac, **options)
        mqtt.start()


class ValveControlCLI:

    @staticmethod
    def run():
        return ValveControlCLI().parse_args()

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('mac', metavar='MAC_ADDRESS', type=str, help="device MAC address")
        self.parser.add_argument(
            'action', metavar='ACTION',
            choices=['status', 'diagnostics', 'open', 'close', 'toggle'],
            default='status',
            help='"status", "diagnostics", "open", "close" or "toggle"',
        )

        self.parser.add_argument('--verbose', '-v', action='store_true', help="verbose mode")

    def parse_args(self, args=None):
        args = self.parser.parse_args(args)

        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(message)s')

        with GFProBluetoothValve(args.mac) as valve:
            if args.action == 'status':
                if valve.is_open():
                    print("Valve is open.")
                else:
                    print("Valve is closed.")

            if args.action == 'diagnostics':
                diagnostics = valve.read_diagnostics()
                print(f"Battery voltage: {diagnostics.battery_voltage}")
                print(f"Battery level: {diagnostics.battery_level}")

            elif args.action == 'toggle':
                valve.toggle_valve()
                if valve.is_open():
                    print("Valve is now open.")
                else:
                    print("Valve is now closed.")

            elif args.action == 'open':
                if valve.is_open():
                    print("Valve is already open")
                else:
                    valve.open_valve()
                    print("Valve opened")

            elif args.action == 'close':
                if not valve.is_open():
                    print("Valve is already closed")
                else:
                    valve.close_valve()
                    print("Valve closed")
