"""
Cricket example program.
Have a temperature sensor plugged into sensor port 2,
and a vibration motor plugged into the first vibration port.


Vibrates as many times as a cricket would have chirpped given the temperature.
"""

from hummingbird import Hummingbird
from time import sleep


humm = Hummingbird()
temp = humm.get_temperature(2)
    
# Convert temperature to number of times to chirp
timesToChirp = int((temp - 4)*3)


# Chirp
while timesToChirp > 0:
    humm.set_vibration_motor(1,200)
    sleep(0.25)
    humm.set_vibration_motor(1,0)
    sleep(0.25)
    timesToChirp -= 1

humm.close()



