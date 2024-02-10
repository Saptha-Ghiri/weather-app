from flask import Flask, render_template, jsonify, request
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

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        city = request.form['city']
    return render_template("index.html")

@app.route('/moni_value')
def moni_value():
    api_key = '6a2b15925e074c1f139105aa6f22db53'
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({'error': 'City name parameter is missing'}), 400
    print(city_name)
    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(base_url)
    weather_data = response.json()
    temp = int(weather_data['main']['temp'] - 273)
    pre = weather_data['main']['pressure']
    humd = weather_data['main']['humidity']
    speed = weather_data['wind']['speed']
    clo = weather_data['weather'][0]['description']
    col_tamil = translate_to_tamil(clo)
    return jsonify({'temp': temp, 'humd': humd, 'pre': pre, 'speed': speed, 'clo': clo, 'tam_clo': col_tamil, 'predicted_whe': 'rainy'})
