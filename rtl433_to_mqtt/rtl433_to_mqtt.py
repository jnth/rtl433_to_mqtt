#!/usr/bin/env python3
# coding: utf-8

"""Convert JSON output of `rtl_433` to MQTT message."""

import json
import subprocess
import random
import string
from typing import Dict, Any, Tuple
import click
import paho.mqtt.client as mqtt


characters = string.ascii_letters * 2 + string.digits


class BaseSensor:
    model = None
    device_id = None

    def __init__(self, data: Dict[str, Any]):
        if self.model is None or self.device_id is None:
            raise ValueError("model and device_id must be set")
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
    device_id = 55

    @property
    def topic(self):
        return "home/sensor/garden/temperature"

    @property
    def json_to_export(self):
        return {'time': self.data['time'], 'battery_ok': self.data['battery_ok'],
                'temperature_C': self.data['temperature_C']}


class PresenceDetectorSensor(BaseSensor):
    model = "Visonic-Powercode"
    device_id = 151

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


def random_id():
    return "".join(random.sample(characters, k=6))


@click.command(help=__doc__)
@click.option("--mqtt-host", default="127.0.0.1", metavar='host', help="MQTT server hostname")
@click.option("--mqtt-port", default=1883, type=int, metavar='port', help="MQTT server port")
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode")
def main(mqtt_host: str, mqtt_port: int, verbose: bool):
    device_ids = [sensor.device_id for sensor in sensors]
    if None in device_ids:
        raise ValueError("Malformed configuration: missing device_id property in one or more sensors.")
    cmd = ["rtl_433", "-F", "json"]
    for device_id in device_ids:
        cmd += ["-R", str(device_id)]

    print("Starting {cmd}".format(cmd=" ".join(cmd)))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        client = mqtt.Client(client_id=f'rtl433-to-mqtt-{random_id()}', clean_session=True)
        client.connect(host=mqtt_host, port=mqtt_port)
        print(f"Connected to MQTT at {mqtt_host}:{mqtt_port}")
        for line in process.stdout:
            topic, payload = process_line(line.decode('utf-8'))
            client.publish(topic, payload, qos=1)
            client.loop()
            if verbose:
                print(f"topic={topic} payload={payload}")
    except KeyboardInterrupt:
        print("Interuption by user")
        return
    except Exception as exc:
        import traceback
        print(f"An exception occurs: {exc}")
        traceback.print_exc()


if __name__ == '__main__':
    main()
