from flask import Flask,render_template, jsonify
import requests
from googletrans import Translator

app = Flask(__name__)

def translate_to_tamil(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='ta')
    return translated_text.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moni_value')
def moni_value():
    api_key = '6a2b15925e074c1f139105aa6f22db53'
    lat = 10.844319296716725# Replace with the actual latitude of your location
    lon =  78.5952864658224  #  # Replace with the actual longitude of your location
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    endpoint_url = f'{base_url}?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(endpoint_url)
    weather_data = response.json()
    temp = int(weather_data['main']['temp'] - 273)
    pre = weather_data['main']['pressure']
    humd = weather_data['main']['humidity']
    speed = weather_data['wind']['speed']
    clo = weather_data['weather'][0]['description']
    col_tamil=translate_to_tamil(clo)
    return jsonify({'temp': temp,'humd': humd,'pre':pre,'speed':speed,'clo':clo,'tam_clo':col_tamil,'predicted_whe':'rainy'})


