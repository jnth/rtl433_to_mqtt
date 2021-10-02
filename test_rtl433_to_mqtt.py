#!/usr/bin/env python3
# coding: utf-8

import unittest
from rtl433_to_mqtt.rtl433_to_mqtt import process_line


class TestProcessing(unittest.TestCase):
    def test_process_thermometer(self):
        line = ('{"time" : "2021-10-12 20:22:44", "model" : "Acurite-606TX", "id" : 14, "battery_ok" : 1, '
                '"temperature_C" : 14.600, "mic" : "CHECKSUM"}')
        topic, payload = process_line(line)
        self.assertEqual(topic, 'home/sensor/outsite/thermometer')
        self.assertEqual(payload, '{"time":"2021-10-12 20:22:44","battery_ok":1,"temperature_C":14.6}')

    def test_process_detector_garage(self):
        line = ('{"time" : "2021-10-12 20:25:32", "model" : "Visonic-Powercode", "id" : "6400bd", "tamper" : 0, '
                '"alarm" : 1, "battery_ok" : 1, "else" : 0, "restore" : 0, "supervised" : 1, "spidernet" : 0, '
                '"repeater" : 0, "mic" : "LRC"}')
        topic, payload = process_line(line)
        self.assertEqual(topic, 'home/sensor/garage/detector')
        self.assertEqual(payload, '{"time":"2021-10-12 20:25:32","battery_ok":1,"alarm":1}')

    def test_process_detector_entrance(self):
        line = ('{"time" : "2021-10-12 20:25:32", "model" : "Visonic-Powercode", "id" : "64f8ab", "tamper" : 0, '
                '"alarm" : 1, "battery_ok" : 1, "else" : 0, "restore" : 0, "supervised" : 1, "spidernet" : 0, '
                '"repeater" : 0, "mic" : "LRC"}')
        topic, payload = process_line(line)
        self.assertEqual(topic, 'home/sensor/entrance/detector')
        self.assertEqual(payload, '{"time":"2021-10-12 20:25:32","battery_ok":1,"alarm":1}')

    def test_process_detector_livingroom(self):
        line = ('{"time" : "2021-10-12 20:25:32", "model" : "Visonic-Powercode", "id" : "a40706", "tamper" : 0, '
                '"alarm" : 1, "battery_ok" : 1, "else" : 0, "restore" : 0, "supervised" : 1, "spidernet" : 0, '
                '"repeater" : 0, "mic" : "LRC"}')
        topic, payload = process_line(line)
        self.assertEqual(topic, 'home/sensor/living-room/detector')
        self.assertEqual(payload, '{"time":"2021-10-12 20:25:32","battery_ok":1,"alarm":1}')


if __name__ == '__main__':
    unittest.main()
