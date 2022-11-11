import json
from math import sin,cos,radians,pi
import matplotlib.pyplot as plt
from constants import *

def process_point_cloud(file_name):
    points = []
    with open(file_name,'r') as f:
        result = json.load(f)
    num_readings = len(result['positions'])
    for i in range(num_readings):
        point_result = calculate_points_from_reading(result['positions'][i],result['readings'][i])
        points = points + point_result

    graph_points(points,result['positions'])
    print(points)
    
def calculate_points_from_reading(position,reading):
    point_result = []
    x = position['x']
    y = position['y']
    heading_r = radians(position['heading'])
    left = reading['left']
    right = reading['right']
    center = reading['center']
    if center<SENSOR_THRESHOLD:
        center_point_x = x+sin(heading_r)*center
        center_point_y = y+cos(heading_r)*center
        point_result.append([center_point_x,center_point_y])
    if right<SENSOR_THRESHOLD:
        right_point_x = x+sin(heading_r+pi/2)*right
        right_point_y = y+cos(heading_r+pi/2)*right
        point_result.append([right_point_x,right_point_y])
    if left<SENSOR_THRESHOLD:
        left_point_x = x+sin(heading_r-pi/2)*left
        left_point_y = y+cos(heading_r-pi/2)*left
        point_result.append([left_point_x,left_point_y])
    return point_result
def graph_points(points,positions):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.scatter(x,y)
    ax = plt.gca()
    ax.set_aspect(1)
    x_position = []
    y_position = []
    for position in positions:
        x_position.append(position['x'])
        y_position.append(position['y'])
    ax.scatter(x_position,y_position)
    plt.show()


if __name__ == '__main__':
    process_point_cloud('results.json')