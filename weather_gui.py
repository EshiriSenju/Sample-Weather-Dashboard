from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtGui import QFontDatabase, QPalette, QColor
from weather_api import WeatherAPI
from datetime import datetime
import requests


class WeatherApp(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api  # Instance of WeatherAPI
        self.is_metric = True  # Flag to track the unit state
        self.load_fonts()  # Load the custom font
        self.initUI()  # Initialize the UI

    def load_fonts(self):
        QFontDatabase.addApplicationFont("path/to/Orbitron-Regular.ttf")

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Sets the color palette for a dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setPalette(palette)

        # Styling
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Orbitron'; 
                font-size: 16px;
                color: #00FF00; 
                background-color: #1C1C1C;
            }
            QLabel, QLineEdit, QPushButton {
                border-style: solid;
                border-width: 2px;
                border-color: #008080;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton {
                color: #00FF00;
                background-color: #333333;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QLineEdit {
                color: #00FF00;
                background-color: #333333;
                font-weight: bold;
            }
        """
        )

        # Widgets
        self.city_entry = QLineEdit(self)
        self.layout.addWidget(self.city_entry, 0, 0, 1, 2)  # Span two columns

        self.get_weather_button = QPushButton("Get Weather", self)
        self.get_weather_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.get_weather_button, 0, 2)

        self.weather_label = QLabel("Weather: ")
        self.layout.addWidget(self.weather_label, 1, 0, 1, 3)  # Span three columns

        self.temperature_label = QLabel("Temperature: ")
        self.layout.addWidget(self.temperature_label, 2, 0)

        self.humidity_label = QLabel("Humidity: ")
        self.layout.addWidget(self.humidity_label, 2, 1)

        self.wind_speed_label = QLabel("Wind Speed: ")
        self.layout.addWidget(self.wind_speed_label, 2, 2)

        self.pressure_label = QLabel("Pressure: ")
        self.layout.addWidget(self.pressure_label, 3, 0)

        self.sunrise_label = QLabel("Sunrise: ")
        self.layout.addWidget(self.sunrise_label, 3, 1)

        self.sunset_label = QLabel("Sunset: ")
        self.layout.addWidget(self.sunset_label, 3, 2)

        self.visibility_label = QLabel("Visibility: ")
        self.layout.addWidget(self.visibility_label, 4, 0)

        self.cloudiness_label = QLabel("Cloudiness: ")
        self.layout.addWidget(self.cloudiness_label, 4, 1)

        self.unit_switch = QPushButton("Switch to Imperial", self)
        self.unit_switch.clicked.connect(self.toggle_units)
        self.layout.addWidget(self.unit_switch, 4, 2)

        self.forecast_label = QLabel("Forecast: ")
        self.layout.addWidget(
            self.forecast_label, 5, 0, 1, 3
        )  # Adjust position as needed

        # Set main window properties
        self.setWindowTitle("Futuristic Weather Dashboard")
        self.setGeometry(300, 300, 600, 400)  # Window size

    def toggle_units(self):
        self.is_metric = not self.is_metric
        self.unit_switch.setText(
            "Switch to Imperial" if self.is_metric else "Switch to Metric"
        )
        self.fetch_weather()

    def fetch_weather(self):
        city = self.city_entry.text()
        if not city.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Input Error", "Please enter a valid city name.")
            return

        try:
            units = "metric" if self.is_metric else "imperial"
            weather_data = self.api.fetch_weather(city, units)

            self.weather_label.setText(
                f"Weather: {weather_data['weather'][0]['description'].capitalize()}"
            )
            self.temperature_label.setText(
                f"Temperature: {weather_data['main']['temp']} °C"
            )
            self.humidity_label.setText(
                f"Humidity: {weather_data['main']['humidity']}%"
            )
            self.wind_speed_label.setText(
                f"Wind Speed: {weather_data['wind']['speed']} m/s"
            )
            self.pressure_label.setText(
                f"Pressure: {weather_data['main']['pressure']} hPa"
            )
            sunrise_time = datetime.fromtimestamp(
                weather_data["sys"]["sunrise"]
            ).strftime("%H:%M")
            sunset_time = datetime.fromtimestamp(
                weather_data["sys"]["sunset"]
            ).strftime("%H:%M")
            self.sunrise_label.setText(f"Sunrise: {sunrise_time}")
            self.sunset_label.setText(f"Sunset: {sunset_time}")

            visibility = weather_data.get("visibility", "N/A")
            cloudiness = weather_data.get("clouds", {}).get("all", "N/A")
            self.visibility_label.setText(
                f"Visibility: {visibility} m"
                if visibility != "N/A"
                else "Visibility: N/A"
            )
            self.cloudiness_label.setText(
                f"Cloudiness: {cloudiness}%"
                if cloudiness != "N/A"
                else "Cloudiness: N/A"
            )

            self.fetch_forecast(city)

        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 404:
                QMessageBox.warning(self, "Error", f"City '{city}' not found.")
            else:
                QMessageBox.warning(self, "HTTP Error", str(errh))
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(
                self,
                "Error",
                "Connection Error. Please check your internet connection.",
            )
        except requests.exceptions.Timeout:
            QMessageBox.warning(self, "Error", "Timeout Error.")
        except requests.exceptions.RequestException as err:
            QMessageBox.warning(self, "Error", "An error occurred: " + str(err))

    def fetch_forecast(self, city):
        try:
            units = "metric" if self.is_metric else "imperial"
            forecast_data = self.api.fetch_forecast(city, units)

            forecast_text = "3-Day Forecast:\n"
            for entry in forecast_data["list"][:3]:  # Just the first 3 entries
                date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d")
                temp = entry["main"]["temp"]
                description = entry["weather"][0]["description"]
                forecast_text += f"{date}: {temp}°C, {description}\n"

            self.forecast_label.setText(forecast_text)

        except Exception as e:
            print("Error fetching forecast:", e)
