class OperatorClient:
    def receive_data(self, device_name, timestamp, data):
        print(f"Operator received data from {device_name}: {data} at {timestamp}")
