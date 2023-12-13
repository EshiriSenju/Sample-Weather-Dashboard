import sys
import requests
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QFontDatabase

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.load_fonts()  # Load the custom font
        self.initUI()

    def load_fonts(self):
        # Load the custom font
        QFontDatabase.addApplicationFont("Orbitron-SemiBold.ttf")

    def initUI(self):
        self.layout = QGridLayout()

        # Set the color palette for a dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setPalette(palette)

        # Styling
        self.setStyleSheet("""
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
        """)

        # Widgets
        self.city_entry = QLineEdit(self)
        self.layout.addWidget(self.city_entry, 0, 0, 1, 2)  # Span two columns

        self.get_weather_button = QPushButton('Get Weather', self)
        self.get_weather_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.get_weather_button, 0, 2)

        self.weather_label = QLabel('Weather: ')
        self.layout.addWidget(self.weather_label, 1, 0, 1, 3)  # Span three columns

        self.temperature_label = QLabel('Temperature: ')
        self.layout.addWidget(self.temperature_label, 2, 0)

        self.humidity_label = QLabel('Humidity: ')
        self.layout.addWidget(self.humidity_label, 2, 1)

        self.wind_speed_label = QLabel('Wind Speed: ')
        self.layout.addWidget(self.wind_speed_label, 2, 2)

        self.pressure_label = QLabel('Pressure: ')
        self.layout.addWidget(self.pressure_label, 3, 0)

        self.sunrise_label = QLabel('Sunrise: ')
        self.layout.addWidget(self.sunrise_label, 3, 1)

        self.sunset_label = QLabel('Sunset: ')
        self.layout.addWidget(self.sunset_label, 3, 2)

        self.visibility_label = QLabel('Viaibility: ')
        self.layout.addWidget(self.visibility_label, 4, 0)

        self.cloudiness_label = QLabel('Cloudiness: ')
        self.layout.addWidget(self.cloudiness_label, 4, 1)

        # Set main window properties
        self.setLayout(self.layout)
        self.setWindowTitle('Futuristic Weather Dashboard')
        self.setGeometry(300, 300, 600, 400)  # Window size

    def fetch_weather(self):
        city = self.city_entry.text()
        api_key = os.getenv('OPENWEATHER_API_KEY')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
            visibility = weather_data.get('visibility', 'N/A')
            cloudiness = weather_data.get('clouds', {}).get("all","N/A")

            self.weather_label.setText(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
            self.temperature_label.setText(f"Temperature: {weather_data['main']['temp']} °C")
            self.humidity_label.setText(f"Humidity: {weather_data['main']['humidity']}%")
            self.wind_speed_label.setText(f"Wind Speed: {weather_data['wind']['speed']} m/s")
            self.pressure_label.setText(f"Pressure: {weather_data['main']['pressure']} hPa")
            sunrise_time = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
            sunset_time = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
            self.sunrise_label.setText(f"Sunrise: {sunrise_time}")
            self.sunset_label.setText(f"Sunset: {sunset_time}")
            self.visibility_label.setText(f"Visibilty: {visibility} m" if visibility!= 'N/A' else "Visibility: N/A")
            self.cloudiness_label.setText(f"Cloudiness: {cloudiness}" if cloudiness!= 'N/A' else "Cloudiness: N/A")

        except requests.exceptions.HTTPError as errh:
            QMessageBox.warning(self, 'Error', f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            QMessageBox.warning(self, 'Error', f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            QMessageBox.warning(self, 'Error', f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            QMessageBox.warning(self, 'Error', f"Error: {err}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
