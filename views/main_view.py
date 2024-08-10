import tkinter as tk
from tkinter import messagebox
from controllers.weather_controller import WeatherController
import logging
import matplotlib.pyplot as plt
from datetime import datetime

logger = logging.getLogger(__name__)


class MainView:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Weather Dashboard")

        # Make the window full screen
        self.root.state('zoomed')

        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=10)

        # Apply a background color
        self.root.configure(bg='#1F51FF')  # Set a blue background

        # Header label
        self.header_label = tk.Label(
            root,
            text="Weather Dashboard",
            font=("Helvetica", 24, "bold"),
            bg='#1F51FF',
            fg='white'
        )
        self.header_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Location entry
        self.location_label = tk.Label(
            root,
            text="Enter Location:",
            font=("Helvetica", 16),
            bg='#1F51FF',
            fg='white'
        )
        self.location_label.grid(row=1, column=0, sticky='e', padx=(0, 10))

        self.location_entry = tk.Entry(
            root,
            font=("Helvetica", 16),
            width=30
        )
        self.location_entry.grid(row=1, column=1, sticky='w', padx=(10, 0))

        # Get weather button
        self.weather_button = tk.Button(
            root,
            text="Get Weather",
            command=self.get_weather,
            font=("Helvetica", 16),
            bg='white',
            fg='#1F51FF'
        )
        self.weather_button.grid(row=2, column=0, pady=20, padx=10)

        # Get forecast button
        self.forecast_button = tk.Button(
            root,
            text="Get Forecast",
            command=self.get_forecast,
            font=("Helvetica", 16),
            bg='white',
            fg='#1F51FF'
        )
        self.forecast_button.grid(row=2, column=1, pady=20, padx=10)

        # Plot forecast button
        self.plot_button = tk.Button(
            root,
            text="Plot Forecast",
            command=self.plot_forecast,
            font=("Helvetica", 16),
            bg='white',
            fg='#1F51FF'
        )
        self.plot_button.grid(row=2, column=2, pady=20, padx=10)

        # Weather information display
        self.weather_info = tk.Text(
            root,
            font=("Helvetica", 14),
            wrap='word',
            bg='white',
            fg='#1F51FF',
            height=20,
            width=80
        )
        self.weather_info.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

        self.weather_controller = WeatherController(api_key)
        self.forecast_data = None  # To store forecast data for plotting

    def get_weather(self):
        location = self.location_entry.get()
        weather_data = self.weather_controller.get_current_weather(location)
        if weather_data:
            self.weather_info.delete('1.0', tk.END)
            weather_info_text = (f"Location: {weather_data.location}\n"
                                 f"Temperature: {weather_data.temperature} °C\n"
                                 f"Humidity: {weather_data.humidity}%\n"
                                 f"Wind Speed: {weather_data.wind_speed} m/s\n"
                                 f"Timestamp: {weather_data.timestamp}")
            self.weather_info.insert(tk.END, weather_info_text)
            self.weather_controller.save_weather_data(weather_data)
        else:
            messagebox.showerror("Error", "Failed to fetch weather data.")

    def get_forecast(self):
        location = self.location_entry.get()
        self.forecast_data = self.weather_controller.get_forecast(location)
        if self.forecast_data:
            self.weather_info.delete('1.0', tk.END)
            forecast_text = "\nForecast:\n"
            for entry in self.forecast_data[:5]:  # Display the first 5 forecast entries
                forecast_text += (f"Time: {entry['dt_txt']}\n"
                                  f"Temp: {entry['main']['temp']} °C\n"
                                  f"Humidity: {entry['main']['humidity']}%\n"
                                  f"Wind Speed: {entry['wind']['speed']} m/s\n"
                                  "-------------------------\n")
            self.weather_info.insert(tk.END, forecast_text)
        else:
            messagebox.showerror("Error", "Failed to fetch forecast data.")

    def plot_forecast(self):
        if not self.forecast_data:
            messagebox.showerror("Error", "No forecast data available to plot.")
            return

        times = [datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S') for entry in self.forecast_data]
        temps = [entry['main']['temp'] for entry in self.forecast_data]
        humidity = [entry['main']['humidity'] for entry in self.forecast_data]
        wind_speeds = [entry['wind']['speed'] for entry in self.forecast_data]

        plt.figure(figsize=(10, 6))

        plt.plot(times, temps, label="Temperature (°C)", color="red", marker='o')
        plt.plot(times, humidity, label="Humidity (%)", color="blue", marker='o')
        plt.plot(times, wind_speeds, label="Wind Speed (m/s)", color="green", marker='o')

        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title("Weather Forecast")
        plt.legend()
        plt.grid(True)

        plt.show()
