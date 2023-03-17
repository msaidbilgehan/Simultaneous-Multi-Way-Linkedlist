

# CLASSES

from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread
from Classes.Node import Node_Struct
from enum import Enum
# from multiprocessing import cpu_count

class COLORS(Enum):
    BLACK = -1
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

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
        
        self.__move_Task_Thread = None

    def set_Color(self, color:COLORS) -> int:
        self.color = color
        return 1

    def get_Color(self) -> COLORS:
        return self.color

    def set_Coordinate(self, x:int, y:int, z:int) -> int:
        self.coordinate_x = x
        self.coordinate_y = y
        self.coordinate_z = z
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
            "color": self.get_Color()
        }
