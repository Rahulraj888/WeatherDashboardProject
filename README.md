# Weather Dashboard Project

A Python desktop application built with Tkinter to display weather data fetched from an external weather API.  
It follows an MVC (Model-View-Controller) architecture for clean separation of concerns.

## Features
- **User Authentication**: Login system for users
- **Current Weather**: View temperature, humidity, wind speed, and conditions for selected locations
- **Search Functionality**: Search weather by city name
- **Data Persistence**: Store user data and preferences in a local SQLite database
- **Modular Architecture**: MVC pattern for better code organization

## Tech Stack
- **Language**: Python 3.x
- **GUI**: Tkinter
- **Database**: SQLite3
- **API**: OpenWeatherMap (or other weather API)
- **Dependencies**: Listed in `requirements.txt`

## Project Structure
```
WeatherDashboardProject-main/
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── config/
│   ├── __init__.py
│   └── local_config.py           # API keys and configuration
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── weather_controller.py
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   └── weather_data.py
├── utils/
│   ├── __init__.py
│   ├── api_client.py             # Handles API calls
│   └── database.py               # SQLite connection
└── views/
    ├── __init__.py
    ├── login_view.py
    └── main_view.py
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd WeatherDashboardProject-main
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   - Open `config/local_config.py`
   - Set your weather API key:
     ```python
     API_KEY = "your_openweathermap_api_key"
     DB_PATH = "weather_dashboard.db"
     ```

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage
- Login or register as a new user
- Search for a city to view its current weather
- View weather statistics and details in the main dashboard

## Notes
- You must have a valid weather API key to fetch live data
- SQLite database file will be created automatically on first run

## License
MIT
