import tkinter as tk
from tkinter import messagebox, filedialog
from controllers.weather_controller import WeatherController
import logging
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

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

        # Header label
        self.header_label = tk.Label(
            root,
            text="Weather Dashboard",
            font=("Helvetica", 24, "bold")
        )
        self.header_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Location entry
        self.location_label = tk.Label(
            root,
            text="Enter Location:",
            font=("Helvetica", 16)
        )
        self.location_label.grid(row=1, column=0, sticky='e', padx=(0, 10))

        self.location_entry = tk.Entry(
            root,
            font=("Helvetica", 16),
            width=30
        )
        self.location_entry.grid(row=1, column=1, sticky='w', padx=(10, 0))

        # Configure grid columns to have equal weight
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

        # Get weather button
        self.weather_button = tk.Button(
            root,
            text="Get Weather",
            command=self.get_weather,
            font=("Helvetica", 16),
            bg='white'
        )
        self.weather_button.grid(row=2, column=0, pady=20, padx=20, sticky='ew')

        # Get forecast button
        self.forecast_button = tk.Button(
            root,
            text="Get Forecast",
            command=self.get_forecast,
            font=("Helvetica", 16),
            bg='white'
        )
        self.forecast_button.grid(row=2, column=1, pady=20, padx=20, sticky='ew')

        # Plot forecast button
        self.plot_button = tk.Button(
            root,
            text="Plot Forecast",
            command=self.plot_forecast,
            font=("Helvetica", 16),
            bg='white'
        )
        self.plot_button.grid(row=2, column=2, pady=20, padx=20, sticky='ew')

        # Load CSV button
        self.load_csv_button = tk.Button(
            root,
            text="Load CSV and Show Insights",
            command=self.load_csv,
            font=("Helvetica", 16),
            bg='white'
        )
        self.load_csv_button.grid(row=2, column=3, pady=20, padx=20, sticky='ew')

        # Weather information display
        self.weather_info = tk.Text(
            root,
            font=("Helvetica", 14),
            wrap='word',
            bg='white',
            height=20,
            width=100
        )
        self.weather_info.grid(row=4, column=0, columnspan=4, padx=20, pady=20)

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

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                insights = self.analyze_csv(df)
                self.weather_info.delete('1.0', tk.END)
                self.weather_info.insert(tk.END, insights)
            except Exception as e:
                logger.error(f"Error reading CSV file: {e}")
                messagebox.showerror("Error", f"Failed to load CSV file.\n{str(e)}")

    def analyze_csv(self, df):
        try:
            # Filter out non-numeric columns for analysis
            numeric_df = df.select_dtypes(include=['number'])

            insights = ""
            insights += "Summary Statistics:\n"
            insights += str(numeric_df.describe()) + "\n\n"

            insights += "Correlation Matrix:\n"
            insights += str(numeric_df.corr()) + "\n\n"

            if 'Rainfall' in df.columns:
                insights += "Rainfall Analysis:\n"
                total_rainfall = df['Rainfall'].sum()
                rain_days = df[df['Rainfall'] > 0].shape[0]
                if rain_days > 0:
                    avg_rainfall = total_rainfall / rain_days
                else:
                    avg_rainfall = 0
                insights += f"Total Rainfall: {total_rainfall} mm\n"
                insights += f"Number of Rainy Days: {rain_days}\n"
                insights += f"Average Rainfall on Rainy Days: {avg_rainfall:.2f} mm\n\n"

            if 'MinTemp' in df.columns and 'MaxTemp' in df.columns:
                insights += "Temperature Trends:\n"
                avg_min_temp = df['MinTemp'].mean()
                avg_max_temp = df['MaxTemp'].mean()
                insights += f"Average Minimum Temperature: {avg_min_temp:.2f} °C\n"
                insights += f"Average Maximum Temperature: {avg_max_temp:.2f} °C\n"

            return insights
        except Exception as e:
            logger.error(f"Error analyzing CSV file: {e}")
            return "Failed to analyze CSV file."
