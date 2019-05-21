

"""
Driver example program.
Connect a motor into motor port 1 and a single LED into LED port 1.

Drives faster when the distance sensor is further away from objects,
and LED is brighter when driving faster.
Stops when an object <12cm away is detected.


"""

from hummingbird import Hummingbird
from time import sleep

humm = Hummingbird()

distance = humm.get_distance(1)

# Drive until object <12cm away detected
while distance > 12:
    humm.set_motor(1,distance/80)
    humm.set_single_led(1,distance*255/80)
        
    sleep(0.1)
        
    distance = humm.get_distance(1)
    print(distance)
humm.close()


