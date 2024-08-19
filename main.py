from sensors import TemperatureSensor, HumiditySensor, RadiationSensor, PressureSensor
from services import ArchivingService, MonitoringService
from clients import OperatorClient
from gui import MonitoringGUI

def main():
    # Create services
    archiving_service = ArchivingService()

    bounds = {
        "Temperature Sensor": (15, 25),  # measured in °C
        "Humidity Sensor": (30, 60),     # measured in %
        "Radiation Sensor": (10, 100),   # measured in  μSv/h
        "Pressure Sensor": (980, 1020)   # measured in hPa
    }

    monitoring_service = MonitoringService(bounds)
    operator_client = OperatorClient()

    # Create sensors
    temp_sensor = TemperatureSensor("Temperature Sensor")
    humidity_sensor = HumiditySensor("Humidity Sensor")
    radiation_sensor = RadiationSensor("Radiation Sensor")
    pressure_sensor = PressureSensor("Pressure Sensor")

    sensors = [temp_sensor, humidity_sensor, radiation_sensor, pressure_sensor]

    # Subscribe services to sensors
    for sensor in sensors:
        sensor.subscribe(archiving_service)
        sensor.subscribe(monitoring_service)
        sensor.subscribe(operator_client)

    # Start GUI
    app = MonitoringGUI(sensors, archiving_service, monitoring_service)
    app.mainloop()

if __name__ == "__main__":
    main()
