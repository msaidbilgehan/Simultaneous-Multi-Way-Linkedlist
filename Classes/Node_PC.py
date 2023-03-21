

# CLASSES

from threading import Thread
from Classes.Node import Node_Struct
from enum import Enum

class COLORS(Enum):
    BLACK = "b"
    WHITE = "w"
    RED = "r"
    GREEN = "g"
    BLUE = "b"
    YELLOW = "y"
    
class MARKERS(Enum):
    X = "x"
    CIRCLE = "o"
    POINT = "."
    TRIANGLE_DOWN = "v"
    TRIANGLE_UP = "^"
    SQUARE = "s"
    PENTAGON = "p"
    PLUS_FILLED = "P"
    STAR = "*"
    DIAMOND = "D"
    THIN_DIAMOND = "d"
    

class Node_Point_Cloud_Struct(Node_Struct):
    def __init__(self, data=None, connections=None, is_Node_Blocked=False):
        super().__init__(
            data=data, 
            connections=connections, 
            is_Node_Blocked=is_Node_Blocked
        )
        self.coordinate_x = 0
        self.coordinate_y = 0
        self.coordinate_z = 0
        
        self.color = COLORS.BLUE
        self.marker = MARKERS.CIRCLE
        self.size = 50
        
        self.__move_Task_Thread = None

    def set_Color(self, color:COLORS) -> int:
        self.color = color
        return 1

    def get_Color(self) -> COLORS:
        return self.color

    def set_Marker(self, marker:MARKERS):
        self.marker = marker

    def get_Marker(self) -> MARKERS:
        return self.marker

    def set_Size(self, size:int):
        self.size = size

    def get_Size(self) -> int:
        return self.size

    def set_Coordinate(self, x:int, y:int, z:int) -> int:
        self.coordinate_x = x
        self.coordinate_y = y
        self.coordinate_z = z
        return 1
    
    def set_Coordinate_X(self, coord: int) -> int:
        self.coordinate_x = coord
        return 1
    
    def set_Coordinate_Y(self, coord: int) -> int:
        self.coordinate_y = coord
        return 1

    def set_Coordinate_Z(self, coord: int) -> int:
        self.coordinate_z = coord
        return 1

    def get_Coordinate(self) -> tuple:
        return self.coordinate_x, self.coordinate_y, self.coordinate_z

    def move(self, x: int = 0, y: int = 0, z: int = 0) -> int:
        self.coordinate_x += x
        self.coordinate_y += y
        self.coordinate_z += z
        return 1
    
    def __move_Task(self, x: int = 0, y: int = 0, z: int = 0, ms: int = 1) -> int:
        while ms != 0:
            ms -= 1
            self.move(x, y, z)
        return 1
    
    def move_Task(self, x: int = 0, y: int = 0, z: int = 0, ms: int = 1) -> int:
        self.__move_Task_Thread = Thread(
            target=self.__move_Task,
            args=[
                x,
                y,
                z,
                ms
            ]
        )
        self.__move_Task_Thread.setDaemon(True)
        self.__move_Task_Thread.start()
        return 1
    
    def get_Information_3D(self):
        return {
            "coordinates": self.get_Coordinate(),
            "color": self.get_Color(),
            "marker": self.get_Marker(),
            "size": self.get_Size(),
            "connected_coordinates": [node.get_Coordinate() for node in self.get_Connected_Node_List()]
        }

    def connect_Node_BiDirection(self, node, relocate: bool = False, x=None, y=None, z=None) -> int:
        if super().connect_Node_BiDirection(node):
            if relocate:
                parent_x, parent_y, parent_z = node.get_Coordinate()
                if x == None:
                    self.set_Coordinate_X(parent_x)
                if y == None:
                    self.set_Coordinate_Y(parent_y)
                if z == None:
                    self.set_Coordinate_Z(parent_z)
            return 1
        else:
            return -1

    def connect_To_Node(self, node, relocate: bool = False, x=None, y=None, z=None) -> int:
        if super().connect_To_Node(node):
            if relocate:
                parent_x, parent_y, parent_z = node.get_Coordinate()
                if x == None:
                    self.set_Coordinate_X(parent_x)
                if y == None:
                    self.set_Coordinate_Y(parent_y)
                if z == None:
                    self.set_Coordinate_Z(parent_z)
            return 1
        else:
            return -1
