import random
from datetime import datetime

class SensorDevice:
    def __init__(self, name):
        self.name = name
        self.state = 'off'
        self.subscribers = []

    def subscribe(self, service):
        self.subscribers.append(service)

    def notify_subscribers(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for subscriber in self.subscribers:
            subscriber.receive_data(self.name, timestamp, data)

    def turn_on(self):
        self.state = 'on'
        print(f"{self.name} turned on.")

    def turn_off(self):
        self.state = 'off'
        print(f"{self.name} turned off.")

    def measure(self):
        if self.state == 'measuring':
            data = self._generate_data()  # Generates new random data
            self.notify_subscribers(data)
            return data
        else:
            return None

    def _generate_data(self):
        raise NotImplementedError("Must implement in subclass.")

class TemperatureSensor(SensorDevice):
    def _generate_data(self):
        data = round(random.uniform(12, 25), 2)
        print(f"TemperatureSensor generated data: {data}")
        return data

class HumiditySensor(SensorDevice):
    def _generate_data(self):
        data = round(random.uniform(25, 60), 2)
        print(f"HumiditySensor generated data: {data}")
        return data

class RadiationSensor(SensorDevice):
    def _generate_data(self):
        data = round(random.uniform(5, 110), 2)
        print(f"RadiationSensor generated data: {data}")
        return data

class PressureSensor(SensorDevice):
    def _generate_data(self):
        data = round(random.uniform(970, 1030), 2)
        print(f"PressureSensor generated data: {data}")
        return data
