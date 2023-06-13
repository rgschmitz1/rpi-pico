from machine import ADC, Pin

class TemperatureSensor:
    # Internal temperature sensor for Raspberry Pi Pico is connected to ADC channel 5
    @property
    def temp(self):
        temp_adc_voltage = ADC(4).read_u16() * (3.3 / 65535)
        return 27 - (temp_adc_voltage - 0.706) / 0.001721

pico_temp_sensor = TemperatureSensor()
# "LED" is a reference to the Raspberry Pi Pico onboard LED
pico_led = Pin("LED", Pin.OUT)