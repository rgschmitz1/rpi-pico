from connection import connect
from json import loads
from machine import reset
from microdot import Microdot
from rpi_pico_w import pico_led, pico_temp_sensor

app = Microdot()

@app.route('/')
def index(request):
    # Open static html file
    with open('index.html', 'r') as file:
        html = file.read()
    rpi_temp = str(pico_temp_sensor.temp)
    rpi_led = 'ON' if pico_led.value() else 'OFF'
    html = html.replace('{rpi_temp}', rpi_temp)
    html = html.replace('{rpi_led}', rpi_led)
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/js/rpi_library.js')
def rpi_js_library(request):
    with open('js/rpi_library.js', 'r') as file:
        return file.read(), 200, {'Content-Type': 'text/javascript'}

@app.route('/led', methods=['POST'])
def rpi_led(request):
    state = request.json['state']
    status = 204
    if state == 'ON':
        pico_led.on()
    elif state == 'OFF':
        pico_led.off()
    else:
        status = 400
    return None, status

@app.route('/temp')
def rpi_temp(request):
    rpi_temp = str(pico_temp_sensor.temp)
    return rpi_temp, 200, {'Content-Type': 'text/plain'}

@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

try:
    pico_led.off()
    connect()
    app.run(debug=True, port=80)
except KeyboardInterrupt:
    reset()