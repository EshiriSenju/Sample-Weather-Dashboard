import sys
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.city_entry = QLineEdit(self)
        self.layout.addWidget(self.city_entry)

        self.get_weather_button = QPushButton('Get Weather', self)
        self.get_weather_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.get_weather_button)

        self.weather_label = QLabel('Weather: ')
        self.layout.addWidget(self.weather_label)

        self.setLayout(self.layout)
        self.setWindowTitle('Weather Dashboard')

    def fetch_weather(self):
        city = self.city_entry.text()
        api_key = os.getenv('OPENWEATHER_API_KEY')  # Make sure to set this environment variable
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
            self.weather_label.setText(f"Weather in {city}: {weather_data['weather'][0]['description'].capitalize()}, Temperature: {weather_data['main']['temp']}°C")
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 404:
                QMessageBox.warning(self, 'Error', f"Weather data for '{city}' not found. Please check the city name.")
            else:
                QMessageBox.warning(self, 'HTTP Error', str(errh))
        except requests.exceptions.ConnectionError as errc:
            QMessageBox.warning(self, 'Connection Error', str(errc))
        except requests.exceptions.Timeout as errt:
            QMessageBox.warning(self, 'Timeout Error', str(errt))
        except requests.exceptions.RequestException as err:
            QMessageBox.warning(self, 'Error', str(err))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
