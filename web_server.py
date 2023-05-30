import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

from secrets import SSID, PASSWORD

def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def serve(connection):
    pico_led.off()
    led_state = "OFF"
    temperature = 0

    # Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass

        if request == '/led/on':
            led_state = "ON"
            pico_led.on()
        elif request == '/led/off':
            led_state = "OFF"
            pico_led.off()
        elif request == '/temp':
            temperature = str(pico_temp_sensor.temp)
            client.send(temperature)
        elif request == '/js/rpi_led.js':
            with open('js/rpi_led.js', 'r') as file:
                client.send(file.read())
        else:
            # Open static html file
            with open('index.html', 'r') as file:
                html = file.read()
            temperature = str(pico_temp_sensor.temp)
            html = html.replace('{rpi_temp}', temperature)
            html = html.replace('{rpi_led}', led_state)
            client.send(html)

        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
