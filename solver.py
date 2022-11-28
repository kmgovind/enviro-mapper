###########################################################################################################
# arguments:
# python solver.py arg1
# arg1 - maze filename. The result will be printed in a new file filename_solved.png
###########################################################################################################

from time import sleep
from PIL import Image 
from enum import Enum
import numpy, sys 

COLOR_BLACK = numpy.array([0, 0, 0, 255])
COLOR_WHITE = numpy.array([255, 255, 255, 255])
COLOR_GREEN = numpy.array([0, 255, 0, 255])
COLOR_RED = numpy.array([255, 0, 0, 255])
COLOR_BLUE = numpy.array([0, 0, 255, 255])  

class Type(Enum):
    FREE= 0
    WALL= 1
    START= 2
    END= 3

class Tile():
    def __init__(self, position, type=Type.FREE):
        self.position = position
        self.g_value = float('inf')
        self.f_value = float('inf')
        self.type = type
        self.parent = None

    def getG(self):
        return self.g_value

    def getF(self):
        return self.f_value

    def setG(self, g):
        self.g_value = g

    def setF(self, f):
        self.f_value = f
    
    def getPosition(self):
        return self.position
    
    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]

    def getType(self):
        return self.type

    def setParent(self, parent):
        self.parent = parent
    
    def getParent(self):
        return self.parent

    def __str__(self):
        if self.getType() == Type.FREE:
            return ' '
        elif self.getType() == Type.WALL:
            return 'X'
        elif self.getType() == Type.START:
            return 'S'
        elif self.getType() == Type.END:
            return 'E'

    def __eq__(self, obj):
        return obj.getPosition() == self.getPosition()

def return_path(last_tile):
    path = []
    current = last_tile
    while current is not None:
        path.append(current.position)
        current = current.getParent()
    return path[::-1]

def heuristic(nearby, endTile):
    return abs(nearby.getX() - endTile.getX()) + abs(nearby.getY() - endTile.getY())

def findRoute(map, startTile, endTile, x_bound, y_bound):
    neighbors = ((0, -1), (0, 1), (-1, 0), (1, 0),(-1, -1), (1,1), (-1, 1), (1, -1))
    open_list = []
    closed_list = []

    startTile.setG(0)
    startTile.setF(heuristic(startTile, endTile))

    open_list.append(startTile)

    while len(open_list) != 0:
        current = open_list[0]
        curr_id = 0
        for id, obj in enumerate(open_list):
            if obj.getF() < current.getF():
                current = obj
                curr_id = id
        
        open_list.pop(curr_id)
        closed_list.append(current)
    
        if current == endTile:
            print('Found solution!')
            return return_path(current)

        nearbyTiles = []
        for offset in neighbors:
            new_pos = (current.getX() + offset[0], current.getY() + offset[1])
            if new_pos[0] >= x_bound or new_pos[0] < 0 or new_pos[1] >= y_bound or new_pos[1] < 0:
                continue

            newTile = map[new_pos[1]][new_pos[0]]
            if newTile.getType() == Type.WALL:
                continue
            nearbyTiles.append(newTile)
        
        for nearby in nearbyTiles:
            temp_g = current.getG() + 1
            if temp_g < nearby.getG():
                nearby.setParent(current)
                nearby.setG(temp_g)
                nearby.setF(nearby.getG() + heuristic(nearby, endTile))

                if len([tile for tile in open_list if nearby == tile]) == 0:
                    open_list.append(nearby)

    print('No results')
    return []


def main():
    map = []
    x = 0
    y = 0

    startTile = None
    endTile = None

    try:
        img = Image.open(sys.argv[1]) 
    except:
        print(f"[ERROR!] Not a valid image found in file: {sys.argv[1]}")
        return
    np_img = numpy.array(img) 

    for row in np_img:
        x = 0
        tmp = []
        for col in row:
            if (col == COLOR_WHITE).all():
                tmp.append(Tile((x, y), Type.FREE))
            elif (col == COLOR_BLACK).all():
                tmp.append(Tile((x, y), Type.WALL))
            elif (col == COLOR_GREEN).all():
                startTile = Tile((x, y), Type.START)
                tmp.append(startTile)
            elif (col == COLOR_RED).all():
                endTile = Tile((x, y), Type.END)
                tmp.append(endTile)
            else:
                print('Err')
                return
            x+=1
        map.append(tmp)
        y+=1

    print(f'Read image {x}x{y}')
    for row in map:
        for col in row:
            print(col, end='')
        print()


    path = findRoute(map, startTile, endTile, x, y)
    print('Path:')
    for index, node in enumerate(path):
        if index != 0 and index != len(path)-1:
            np_img[node[1]][node[0]] = COLOR_BLUE
            print(node)
    im = Image.fromarray(np_img)

    filename = (sys.argv[1]).rsplit('.', 1)[0]
    im.save(filename+"_solved.png")

if __name__ == '__main__':
    main()


