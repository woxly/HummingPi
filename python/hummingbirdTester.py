

"""
Hummingbird Tester
Uses every API call from the Hummingbird API


"""

from hummingbird import Hummingbird
from time import sleep

humm = Hummingbird()

# Print sensor values (note this assumes the proper sensors are connected)
sensor_one, sensor_two, sensor_three, sensor_four = humm.get_all_sensors()
print(sensor_one)
print(sensor_two)
print(sensor_three)
print(sensor_four)

distance = humm.get_distance(1)
temperature = humm.get_temperature(2)
light = humm.get_light_sensor(3)
sound = humm.get_sound_sensor(4)
knob = humm.get_knob_value(4)
raw = humm.get_raw_sensor_value(4)
motor_power = humm.are_motors_powered()
print(distance)
print(temperature)
print(light)
print(sound)
print(knob)
print(raw)
print(motor_power)

i = 1;

while i < 5:
    humm.set_servo(i, 90)
    humm.set_single_led(i, 255)
    i+=1

i = 1;

while i < 3:
    humm.set_tricolor_led(i, 255, 255, 255)
    humm.set_motor(i, 0.5)
    humm.set_vibration_motor(i, 127)
    i+=1

sleep(3)
humm.halt()
humm.set_all_motors(-1.0, -1.0)
sleep(2)
humm.close()


