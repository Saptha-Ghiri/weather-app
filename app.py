from flask import Flask, render_template, jsonify, request
import requests
from googletrans import Translator
global city
import cv2
city = ""
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
        global city
        city = request.form['city']
        print("Received city name:", city)  # Add this print statement
    return render_template("index.html")

@app.route('/moni_value')
def moni_value():
    api_key = '6a2b15925e074c1f139105aa6f22db53'
    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(base_url)
    if response.status_code == 404 or len(city)==0:
        return jsonify({'error':"City is not found"})
    try:
        weather_data = response.json()
        temp = int(weather_data['main']['temp'] - 273)
        pre = weather_data['main']['pressure']
        humd = weather_data['main']['humidity']
        speed = weather_data['wind']['speed']
        clo = weather_data['weather'][0]['description']
        vis = weather_data['visibility']
        col_tamil = translate_to_tamil(clo)
        return jsonify({'temp': temp, 'humd': humd, 'pre': pre, 'speed': speed, 'clo': clo, 'tam_clo': col_tamil, 'predicted_whe': 'rainy','city_name':city,"visibility":vis})
    except Exception as e:
        return jsonify({'error':"City is not found"})


# Route to display the video stream on the webpage
# Function to capture video from the camera
def capture_video():
    camera = cv2.VideoCapture(0)  # 0 represents the default camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()

# Route to display the video stream on the webpage
@app.route('/cam')
def cam():
    return render_template('cam.html')

# Function to stream the video
@app.route('/video_feed')
def video_feed():
    return Response(capture_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

    

