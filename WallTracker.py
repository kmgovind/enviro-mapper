
from math import sin, cos
#from compass import return_heading
from ultrasonic import get_all_distance
import json


class WallTracker():
    def __init__(self) -> None:
        self.X = 0
        self.Y = 0
        self.heading = 0
        self.readings = []
        self.positions = []
        
    def take_reading_move_forward(self,cmMoved):
        ultrasonic_result = get_all_distance()
        #compass_result = return_heading()
        x_movement = cmMoved*sin(self.heading)
        y_movement = cmMoved*cos(self.heading)
        self.X = self.X +x_movement
        self.Y = self.Y + y_movement
        self.positions.append({'x':self.X,'y':self.Y,'heading':self.heading})
        self.readings.append(ultrasonic_result)


    def take_reading_turn(self,degreesTurned):
        ultrasonic_result = get_all_distance()
        #compass_result = return_heading()
        self.heading = self.heading + degreesTurned
        self.positions.append({'x':self.X,'y':self.Y,'heading':self.heading})
        self.readings.append(ultrasonic_result)

    def export_results(self,file_name):
        jsonObject = {'positions':self.positions,'readings': self.readings}
        with open("results.json",'w') as f:
            f.write(json.dumps(jsonObject))
