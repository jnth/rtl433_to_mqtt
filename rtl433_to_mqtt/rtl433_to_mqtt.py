#!/usr/bin/env python3
# coding: utf-8

"""Convert JSON output of `rtl_433` to MQTT message."""

import sys
import json
from typing import Dict, Any, Tuple
import click
import paho.mqtt.client as mqtt


class BaseSensor:
    model = None

    def __init__(self, data: Dict[str, Any]):
        if self.model is None:
            raise ValueError("model must be set")
        self.data = data

    @property
    def topic(self):
        """MQTT topic."""
        raise NotImplementedError()

    @property
    def json_to_export(self):
        """JSON to export with MQTT."""
        raise NotImplementedError()

    def to_json(self):
        return json.dumps(self.json_to_export, separators=(',', ':'))


class ThermometerSensor(BaseSensor):
    model = "Acurite-606TX"

    @property
    def topic(self):
        return "home/sensor/garden/temperature"

    @property
    def json_to_export(self):
        return {'time': self.data['time'], 'battery_ok': self.data['battery_ok'],
                'temperature_C': self.data['temperature_C']}


class PresenceDetectorSensor(BaseSensor):
    model = "Visonic-Powercode"

    location_ids = {
        'a40706': 'living-room',
        '64f8ab': 'entrance',
        '6400bd': 'garage',
    }

    @property
    def topic(self):
        location = self.location_ids[self.data['id']]
        return f"home/sensor/{location}/detector"

    @property
    def json_to_export(self):
        return {'time': self.data['time'], 'battery_ok': self.data['battery_ok'], 'alarm': self.data['alarm']}


# Register sensors
sensors = [ThermometerSensor, PresenceDetectorSensor]


def process_line(line: str) -> Tuple[str, str]:
    data = json.loads(line)
    for sensor in sensors:
        if sensor.model is None:
            raise ValueError(f"Malformed configuration of {sensor.__name__}: missing model property.")
        if sensor.model == data['model']:
            sensor_instance = sensor(data)
            return sensor_instance.topic, sensor_instance.to_json()


@click.command(help=__doc__)
@click.option("--mqtt-host", default="127.0.0.1", metavar='host', help="MQTT server hostname")
@click.option("--mqtt-port", default=1883, type=int, metavar='port', help="MQTT server port")
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode")
def main(mqtt_host: str, mqtt_port: int, verbose: bool):
    try:
        client = mqtt.Client(client_id='rtl433-to-mqtt', clean_session=True)
        client.connect(host=mqtt_host, port=mqtt_port)
        print(f"Connected to MQTT at {mqtt_host}:{mqtt_port}")
        for line in sys.stdin:
            topic, payload = process_line(line)
            client.publish(topic, payload, qos=1)
            if verbose:
                print(f"topic={topic} payload={payload}")
    except Exception as exc:
        import traceback
        print(f"An exception occurs: {exc}")
        traceback.print_exc()


if __name__ == '__main__':
    main()
