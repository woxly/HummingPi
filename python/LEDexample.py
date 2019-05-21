
"""
Example LED program.
Plug in a single colored LED into port 1, a tri colored LED into tri-color
port 2, a motor into motor port 1, a sound sensor in port 4, and
a distance sensor into port 1.
Place the distance sensor so it will not detect anything within 80cm of itself.
To exit out of the program, move your hand in front of the distance sensor.
"""


from hummingbird import Hummingbird
from time import sleep

humm = Hummingbird()
distance = humm.get_distance(1)
# Loop until object <20cm away detected
while distance > 20:
    # Get sound reading
    sound = humm.get_raw_sensor_value(4)

    # Set motor and leds
    humm.set_motor(1,sound/255)
    humm.set_single_led(1,sound)
    humm.set_tricolor_led(2,sound, 255-sound, sound)

    sleep(0.2)
    distance = humm.get_distance(1)
    print(distance)

humm.close()
