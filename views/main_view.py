import tkinter as tk
from tkinter import messagebox
from controllers.weather_controller import WeatherController
import logging

logger = logging.getLogger(__name__)


class MainView:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Weather Dashboard")
        self.weather_controller = WeatherController(api_key)

        self.location_label = tk.Label(root, text="Location")
        self.location_label.pack()
        self.location_entry = tk.Entry(root)
        self.location_entry.pack()

        self.weather_button = tk.Button(root, text="Get Weather", command=self.get_weather)
        self.weather_button.pack()

        self.weather_info = tk.Text(root)
        self.weather_info.pack()

    def get_weather(self):
        location = self.location_entry.get()
        weather_data = self.weather_controller.get_current_weather(location)
        if weather_data:
            self.weather_info.delete('1.0', tk.END)
            weather_info_text = (f"Location: {weather_data['location']}\n"
                                 f"Temperature: {weather_data['temperature']} °C\n"
                                 f"Humidity: {weather_data['humidity']}%\n"
                                 f"Wind Speed: {weather_data['wind_speed']} m/s\n"
                                 f"Timestamp: {weather_data['timestamp']}")
            self.weather_info.insert(tk.END, weather_info_text)
            self.weather_controller.save_weather_data(**weather_data)
        else:
            messagebox.showerror("Error", "Failed to fetch weather data.")
