import requests
import certifi
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from datetime import datetime

API_KEY = '5f2ab9011635a307e29aaa7900eeb68f'  # Your OpenWeatherMap API Key

class WeatherApp(App):
    def build(self):
        self.outer_layout = FloatLayout()
        self.outer_layout.canvas.before.clear()
        with self.outer_layout.canvas.before:
            Color(0, 0, 0, 1)  # Black background
            self.rect = Rectangle(size=self.outer_layout.size, pos=self.outer_layout.pos)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint=(None, None), size=(600, 400))
        self.layout.bind(size=self._update_canvas)

        # Welcome label at the top with bigger font size
        self.welcome_label = Label(text='Hoş Geldiniz! Lütfen bir şehir girin.', 
                                    size_hint=(1, None), height=100, 
                                    font_size=48, color=(1, 1, 1, 1),  # Increased font size
                                    halign='center', valign='middle')
        self.welcome_label.bind(size=self.welcome_label.setter('text_size'))
        self.layout.add_widget(self.welcome_label)

        # City input
        self.city_input = TextInput(multiline=False, size_hint_y=None, height=60, 
                                     font_size=24, background_color=(1, 1, 1, 1), 
                                     foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.city_input)

        # Get weather button
        self.get_weather_button = Button(text='Hava Durumunu Al', size_hint_y=None, 
                                          height=50, font_size=24, 
                                          background_color=(1, 1, 1, 1), 
                                          color=(0, 0, 0, 1))
        self.get_weather_button.bind(on_press=self.get_weather)
        self.layout.add_widget(self.get_weather_button)

        # Center the main layout in the FloatLayout
        self.outer_layout.add_widget(self.layout)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Version label
        self.version_label = Label(text='Versiyon: 1.0.0.0', size_hint=(None, None), size=(200, 30), 
                                   font_size=18, color=(1, 1, 1, 1))
        self.version_label.pos_hint = {'right': 1, 'bottom': 0}  # Position it at the bottom right
        self.outer_layout.add_widget(self.version_label)

        return self.outer_layout

    def _update_canvas(self, instance, size):
        self.outer_layout.canvas.before.clear()
        with self.outer_layout.canvas.before:
            Color(0, 0, 0, 1)  # Black background
            self.rect = Rectangle(size=self.outer_layout.size, pos=self.outer_layout.pos)

    def get_weather(self, instance):
        city = self.city_input.text
        if city:
            self.outer_layout.remove_widget(self.welcome_label)  # Remove welcome label
            self.weather = self.fetch_weather(city)
            if self.weather:
                result_text = (
                    f"Şehir: {self.weather['city']}\n"
                    f"Sıcaklık: {self.weather['temperature']} °C\n"
                    f"Nem: {self.weather['humidity']}%\n"
                    f"Rüzgar Hızı: {self.weather['wind_speed']} m/s\n"
                    f"Hava Durumu: {self.weather['description']}\n"
                    f"Güneş Doğumu: {self.weather['sunrise']}\n"
                    f"Güneş Batımı: {self.weather['sunset']}\n"
                )
                self.result_label = Label(text=result_text, size_hint_y=None, height=300, 
                                           font_size=24, halign='center', valign='middle', 
                                           color=(1, 1, 1, 1))
                self.result_label.bind(size=self.result_label.setter('text_size'))
                self.layout.add_widget(self.result_label)
            else:
                self.show_popup("Hata", "Şehir bulunamadı. Lütfen tekrar deneyin.")

    def fetch_weather(self, city):
        try:
            # Fetch weather data from OpenWeatherMap API
            response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric',
                verify=certifi.where()  # Use certifi for SSL verification
            )
            print("Response Status Code:", response.status_code)  # Debugging
            print("Response Content:", response.content)  # Debugging

            data = response.json()
            if response.status_code == 200:
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

                return {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'description': data['weather'][0]['description'],
                    'sunrise': sunrise,
                    'sunset': sunset
                }
            else:
                return None
        except Exception as e:
            print("Error fetching weather data:", e)
            return None

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    WeatherApp().run()
