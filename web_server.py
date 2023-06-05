import network
import socket
from json import loads
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
    rpi_led = 'OFF'
    rpi_temp = 0

    # Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024).decode('utf8')

        try:
            method = request.split()[0]
            route = request.split()[1]
        except IndexError:
            pass

        # Response header is expected
        response_header = 'HTTP/2.0 200 OK\nContent-Type: text/html; encoding=utf8\n\n'
        if method == 'POST':
            if route == '/led':
                state = loads(request.split()[-1])['state']
                response_header = b'HTTP/2.0 204 No Content\n'
                if state == 'ON':
                    pico_led.on()
                elif state == 'OFF':
                    pico_led.off()
                else:
                    response_header = b'HTTP/2.0 400 Bad Request\n'
                client.send(response_header)
        elif method == 'GET':
            if route == '/temp':
                rpi_temp = str(pico_temp_sensor.temp)
                response_header = response_header.replace('html', 'plain')
                client.send(response_header.encode('utf-8'))
                client.send(rpi_temp)
            # Send static page after modifying temperature and led state
            elif route == '/':
                # Open static html file
                with open('index.html', 'r') as file:
                    html = file.read()
                rpi_temp = str(pico_temp_sensor.temp)
                html = html.replace('{rpi_temp}', rpi_temp)
                html = html.replace('{rpi_led}', rpi_led)
                client.send(response_header.encode('utf-8'))
                client.sendall(html)
            # JavaScript for setting pico LED and checking temperature
            elif route == '/js/rpi_library.js':
                with open('js/rpi_library.js', 'r') as file:
                    response_header = response_header.replace('html', 'javascript')
                    client.send(response_header.encode('utf-8'))
                    client.sendall(file.read())

        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
