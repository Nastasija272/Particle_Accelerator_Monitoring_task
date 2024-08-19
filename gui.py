import tkinter as tk
from tkinter import ttk
from datetime import datetime


class MonitoringGUI(tk.Tk):
    def __init__(self, sensors, archiving_service, monitoring_service):
        super().__init__()
        self.title("Particle Accelerator Monitoring System")
        self.geometry("800x600")
        self.sensors = sensors
        self.archiving_service = archiving_service
        self.monitoring_service = monitoring_service

        self.create_widgets()

    def create_widgets(self):
        self.sensor_frames = {}
        for sensor in self.sensors:
            frame = ttk.LabelFrame(self, text=sensor.name)
            frame.pack(fill="x", padx=10, pady=5)
            label = ttk.Label(frame, text="No data yet", font=("Helvetica", 14))
            label.pack(padx=10, pady=10)
            self.sensor_frames[sensor.name] = label

        # Create a button to show archived data
        archive_button = ttk.Button(self, text="Show Archives", command=self.show_archives)
        archive_button.pack(pady=10)

        # Create a frame for control buttons
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=5)

        # Create a button to start all sensors
        self.start_button = ttk.Button(control_frame, text="Start All Sensors", command=self.start_all_sensors)
        self.start_button.pack(side="left", padx=5)

        # Create a button to stop all sensors
        self.stop_button = ttk.Button(control_frame, text="Stop All Sensors", command=self.stop_all_sensors)
        self.stop_button.pack(side="left", padx=5)

        # Create a label to display the current alarm state
        self.alarm_label = ttk.Label(self, text="", font=("Helvetica", 16))
        self.alarm_label.pack(pady=10)

    def start_all_sensors(self):
        # Turn on and start measuring for each sensor
        for sensor in self.sensors:
            sensor.turn_on()
            sensor.state = 'measuring'
            self.update_sensor_display(sensor)  # Update display for each sensor

    def stop_all_sensors(self):
        # Turn off all sensors and update the display to show "Stopped"
        for sensor in self.sensors:
            sensor.turn_off()
            self.sensor_frames[sensor.name].config(text="Stopped")

    def update_sensor_colors(self):
        # Get the current alarm state and faulty sensors from the monitoring service
        alarm_state = self.monitoring_service.get_alarm_state()
        faulty_sensors = self.monitoring_service.get_faulty_sensors()

        if alarm_state == "EMERGENCY ALARM":
            # Set the background color of all sensor labels to red for emergency alarm
            for label in self.sensor_frames.values():
                label.config(background='red')
            self.alarm_label.config(text=f"EMERGENCY ALARM! Faulty Sensors: {', '.join(faulty_sensors.keys())}", background='red')
        elif alarm_state == "ALARM FAULTY SENSOR":
            # Set the background color to yellow for faulty sensors, green for others
            for sensor_name, label in self.sensor_frames.items():
                if sensor_name in faulty_sensors:
                    label.config(background='yellow')
                else:
                    label.config(background='green')
            self.alarm_label.config(text=f"FAULTY SENSOR ALARM! Faulty Sensors: {', '.join(faulty_sensors.keys())}", background='yellow')
        else:
            # Set the background color of all sensor labels to green when no alarm
            for label in self.sensor_frames.values():
                label.config(background='green')
            self.alarm_label.config(text="", background=self.cget('background'))

    def update_sensor_display(self, sensor):
        if sensor.state == 'measuring':
            value = sensor.measure()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Define measurement units for each sensor type
            if sensor.name == "Temperature Sensor":
                unit = "°C"
            elif sensor.name == "Humidity Sensor":
                unit = "%"
            elif sensor.name == "Radiation Sensor":
                unit = "μSv/h"
            elif sensor.name == "Pressure Sensor":
                unit = "hPa"
            else:
                unit = "Unit"

            text = f"Time: {timestamp}\nData: {value} {unit}"

            # Update the sensor display
            self.sensor_frames[sensor.name].config(text=text)

            # Print debugging information
            print(f"\nUpdating {sensor.name}:")
            print(f"  Value: {value}")
            print(f"  Alarm Triggered: {self.monitoring_service.get_alarm_state()}")
            print(f"  Faulty Sensors: {self.monitoring_service.get_faulty_sensors()}")
            print("-" * 35)

            # Update sensor colors based on alarm state
            self.update_sensor_colors()

            # Schedule the next update
            self.after(3000, lambda: self.update_sensor_display(sensor))

    def show_archives(self):
        archive_window = tk.Toplevel(self)
        archive_window.title("Archived Data")
        archive_window.geometry("600x400")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(archive_window)
        scrollbar = ttk.Scrollbar(archive_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create a window inside the canvas to hold the scrollable frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add the archived data to the scrollable frame
        for sensor_name, data in self.archiving_service.archive.items():
            frame = ttk.LabelFrame(scrollable_frame, text=sensor_name)
            frame.pack(fill="x", padx=10, pady=5)
            for entry in data:
                timestamp, value = entry

                if sensor_name == "Temperature Sensor":
                    unit = "°C"
                elif sensor_name == "Humidity Sensor":
                    unit = "%"
                elif sensor_name == "Radiation Sensor":
                    unit = "μSv/h"
                elif sensor_name == "Pressure Sensor":
                    unit = "hPa"
                else:
                    unit = "Unit"

                # Display the measurement with the appropriate unit
                label_text = f"Time: {timestamp}, Value: {value} {unit}"
                label = ttk.Label(frame, text=label_text)
                label.pack(padx=10, pady=5)