# Functions to control the Hummingbird controller.

# The Hummingbird is a robotics kit to promote engineering and arts education, resulting from
# the Arts & Bots research program at Carnegie Mellon's CREATE lab.
# http://www.hummingbirdkit.com
# See included examples and documentation for how to use the API

import time
import hummingbirdconnection

class Hummingbird():

    def __init__(self):
        self.connection = hummingbirdconnection.ThreadedHummConnection()
        self.connection.open()
        self.get_all_sensors() # first sensor read sometimes provides incorrect results, so we do one immediately

    def set_tricolor_led(self, light, *args):
        """Control the two tricolored LEDs (orbs).
        First argument is which port, second is the color.

        
          - hex triplet string: led(1,'#00FF8B')
          - 0-255 RGB values: led(1,0, 255, 139)
          - light = 1 for LED 1, light = 2 for LED 2
        """
        if len(args) == 3:
            r, g, b = [int(x) % 256 for x in args]
        elif (len(args) == 1 and isinstance(args[0], str)):
            color = args[0].strip()
            if len(color) == 7 and color.startswith('#'):
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
        else:
            return
        
        if (light == 1):
            self.connection.send(b'O', [ord('0'), r, g, b]) # 0 is port 1, 1 is port 2 on Hummingbird
        else:
            self.connection.send(b'O', [ord('1'), r, g, b])
            
    def set_single_led(self, light, intensity):
        """Controls the single colored LED's
        First argument is which port, second is intensity.

          -light: control which light, from 1-4
          -intensity: set the intensity of the light from 0 to 255
        """
        
        corrected_light = (int(light) -1) % 4 + 48 # We're adding 48 as this is the unicode value of '0'
        self.connection.send(b'L', [corrected_light, int(intensity)%256])

    def set_motor(self, motor, speed):
        """Controls the two motors

          -motor: 1 for motor 1, 2 for motor 2
          -speed: Values must range from -1.0 (full throttle revers) to
          1.0 (full throttle forward).
        """
        corrected_motor = (int(motor) - 1)%2 + 48
        corrected_direction = int((speed)<0) + 48
        corrected_speed = min(abs(int(speed*255)),255)
        self.connection.send(b'M', [corrected_motor, corrected_direction, corrected_speed])

    def set_all_motors(self,speedone, speedtwo):
        """Controls both motors at the same time

          -speedone: Speed for motor one, values must range from -1.0 (full throttle reverse) to
          1.0 (full throttle forward).
          -speedtwo: Speed for motor two, values must range from -1.0 (full throttle reverse) to
          1.0 (full throttle forward).
        """
        self.set_motor(1,speedone)
        self.set_motor(2,speedtwo)

    def set_vibration_motor(self, motor, intensity):
        """Controls the vibration of the two motors
        First argument is which port, second is intensity.

          -motor: 1 for motor 1, 2 for motor 2
          -intensity: 0 (slowest) - 255(fastest)
        """
        corrected_motor = (int(motor) - 1)%2 + 48
        corrected_intensity = (int(intensity) %256)
        self.connection.send(b'V', [corrected_motor, corrected_intensity])

    def set_servo(self, port, angle):
        """Controls the angle of the servos

          -port: 1 for port 1, 2 for port 2, 3 for port 3, 4 for port 4
          -angle: value between 0 - 180
        """
        corrected_port = (int(port) - 1)%4 + 48
        corrected_angle = (int(angle*230/180))%231
        self.connection.send(b'S', [corrected_port, corrected_angle])

    def get_raw_sensor_value(self, port):
        """Gets the reading of the specified port.

          -port: 1 for port 1, 2 for port 2, 3 for port 3, 4 for port 4
          -returns: a float between 0 - 255, 0 corresponds to 0V, 255 corresponds
          to 5V, increases linearly.
        """
        corrected_port = (int(port) - 1)%4 + 48
        self.connection.send(b's', [corrected_port])
        data = self.connection.receive()
        if data is not None:
            return data[0]

    def get_light_sensor(self,port):
        """See get_raw_sensor_value"""
        return self.get_raw_sensor_value(port)

    def get_knob_value(self,port):
        """See get_raw_sensor_value"""
        return self.get_raw_sensor_value(port)

    def get_sound_sensor(self,port):
        """See get_raw_sensor_value"""
        return self.get_raw_sensor_value(port)

    def get_temperature(self, port):
        """Gets the temperature (C) of the specified port.

          -REQUIRES: Given port has temperature sensor plugged in.
          -port: 1 for port 1, 2 for port 2, 3 for port 3, 4 for port 4
          -returns: A temperature in C.
        """
        raw_temp = self.get_raw_sensor_value(port)
        return int((raw_temp - 127)/2.4+25)

    def get_distance(self,port):
        """Gets the distance (cm) of the specified port.

          -REQUIRES: Given port has distance sensor plugged in.
          -port: 1 for port 1, 2 for port 2, 3 for port 3, 4 for port 4
          -returns: A distance in cm.
        """
        raw_distance = self.get_raw_sensor_value(port)
        if raw_distance < 23:
            return 80
        else:
            temp = 206.76903754529479 - 9.3402257299483011 * raw_distance
            temp += 0.19133513242939543 * pow(raw_distance, 2)
            temp -= 0.0019720997497951645 * pow(raw_distance, 3)
            temp += 9.9382154479167215 * pow(10,-6) * pow(raw_distance, 4) 
            temp -= 1.9442731496914311 * pow(10, -8) * pow(raw_distance, 5)
            if temp < 8:
                temp = 8
            return int(temp)

    def get_all_sensors(self):
        """Gets the reading of all four Hummingbird sensor ports

          -returns: four floats between 0 - 255, 0 corresponds to 0V, 255 corresponds
          to 5V, increases linearly.
        """
        self.connection.send(b'G', [51]) # 51 is the unicode value of ascii 3
        data = self.connection.receive()
        if data is not None:
            one = data[0]
            two = data[1]
            three = data[2]
            four = data[3]
            return one, two, three, four

    def are_motors_powered(self):
        """Detects if motor power is plugged in

          -returns: true if they're plugged in, false otherwise 
        """
        self.connection.send(b'G', [51]) # 51 is the unicode value of ascii 3
        data = self.connection.receive()
        if data is not None:
            if data[4] == 1:
                return True
            else:
               return False

    def halt(self):
        """ Set all motors and LEDs to off. """
        self.connection.send(b'X', [0])

    def close(self):
        self.connection.close()
