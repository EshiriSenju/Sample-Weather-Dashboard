import sys
from PyQt5.QtWidgets import QApplication
from weather_gui import WeatherApp
from weather_api import WeatherAPI
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ap = WeatherAPI(api_key=os.getenv('OPENWEATHER_API_KEY'))
    ex = WeatherApp(api)
    ex.show()
    sys.exit(app.exec_())
