class ArchivingService:
    def __init__(self):
        self.archive = {}

    def receive_data(self, device_name, timestamp, data):
        if device_name not in self.archive:
            self.archive[device_name] = []
        self.archive[device_name].append((timestamp, data))


class MonitoringService:
    def __init__(self, bounds, fault_tolerance=1):
        self.bounds = bounds
        self.fault_tolerance = fault_tolerance
        self.faulty_sensors = {}

    def receive_data(self, device_name, timestamp, data):
        min_value, max_value = self.bounds.get(device_name, (float('-inf'), float('inf')))

        if data < min_value or data > max_value:
            self.handle_faulty_sensor(device_name, timestamp, data)
        else:
            # Remove sensor from faulty list if it is within bounds
            self.faulty_sensors.pop(device_name, None)

        # Update alarm state based on the number of faulty sensors
        self.update_alarm_state()

    def handle_faulty_sensor(self, device_name, timestamp, data):
        # Add or update the faulty sensor data
        self.faulty_sensors[device_name] = (timestamp, data)
        self.log_faulty_sensor(device_name, timestamp, data)

    def update_alarm_state(self):
        # Determine alarm state based on the number of faulty sensors
        if len(self.faulty_sensors) > 1:
            self.alarm_state = "EMERGENCY ALARM"
        elif len(self.faulty_sensors) == 1:
            self.alarm_state = "ALARM FAULTY SENSOR"
        else:
            self.alarm_state = "NORMAL"
        # Log the current alarm state and the list of faulty sensors
        self.log_alarm_state()

    def log_faulty_sensor(self, device_name, timestamp, data):
        print("===================================")
        print(f"FAULTY SENSOR DETECTED:")
        print(f"  Sensor Name:   {device_name}")
        print(f"  Time:          {timestamp}")
        print(f"  Value:         {data}")
        print("===================================")

    def log_alarm_state(self):
        print("-----------------------------------")
        print(f"CURRENT ALARM STATE: {self.alarm_state}")
        if self.faulty_sensors:
            print("FAULTY SENSORS LIST:")
            for device_name, (timestamp, data) in self.faulty_sensors.items():
                print(f"  - {device_name} | Time: {timestamp} | Data: {data}")
        else:
            print("No faulty sensors detected.")
        print("-----------------------------------\n")

    def get_alarm_state(self):
        return self.alarm_state

    def get_faulty_sensors(self):
        return self.faulty_sensors

