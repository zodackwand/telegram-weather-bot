import telebot
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if TOKEN is None:
    raise ValueError("TELEGRAM_API_TOKEN is not set in the environment variables.")

# connecting a bot token
bot = telebot.TeleBot(TOKEN)

# starting message init
starting_text = "Hello and welcome to the bot! Type a city name to find out the temperature."
error_text = "Sorry, we couldn't find this city. Try once again."

# command to handle /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, starting_text, parse_mode='Markdown')

# command to handle any other input as a city name
@bot.message_handler(content_types=['text'])
def weather(message):
    # get a city name from input
    city = message.text
    global user_id
    user_id = message.from_user.id
    # creating a request
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4061cb5c0adc4fb551fcc3d6b13929c0&units=metric'
    # sending the request
    weather_data = requests.get(url).json()
    # unpacking data from the request
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    # creating responses for the user
    weather_now = f"The temperature now is: {temperature} °C"
    weather_feels = f"It feels like: {temperature_feels} °C"

    # sending the responses to the user
    bot.send_message(message.from_user.id, weather_now)
    bot.send_message(message.from_user.id, weather_feels)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print("Exception!")
            bot.send_message(user_id, error_text)