

# CLASSES

import threading


class Node_Struct(object):
    id_counter = 0

    def __init__(self, data=None, connections=None, is_Node_Blocked=False, task_Sleep_Time=0):
        connections = [] if connections is None else connections

        # Self Checker
        if self in connections:
            raise Exception("Node can't be connected to itself")

        self.data = data
        
        self.id = self.id_counter
        
        # Node Block Status
        self.is_Node_Blocked = is_Node_Blocked
        
        # Exit Statement for Threading
        self.exit_Statement = False
        
        # Process Time (in seconds)
        self.task_Sleep_Time = task_Sleep_Time

        # Node Position
        self.connected_Node_List = connections
        
        # To ensure there will be no rise condition between threads at searching (DO NOT USE DIRECTLY)
        self.__thread_list = list()

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, *args, **kwargs):
        # Node ID
        # cls.id_counter += 1
        Node_Struct.id_counter += 1
        return super(Node_Struct, cls).__new__(cls, *args, **kwargs)
    
    def task(self, args):
        # Override this method
        # Do Something
        pass

    def task_Start(self, task, args):
        self.__thread_list.append(
            threading.Thread(
                target=task,
                args=args
            )
        )
        self.__thread_list[-1].start()
        
    def task_Stop(self):
        self.exit_Statement = True

    def connect_Two_Way_Node(self, node):
        self.connected_Node_List.append(node)
        node.connected_Node_List.append(node)

    def disconnect_Two_Way_Node(self, node):
        self.connected_Node_List.remove(node)
        node.connected_Node_List.remove(self)
        
    def connect_To_Node(self, node):
        self.connected_Node_List.append(node)
        
    def disconnect_From_Node(self, node):
        self.connected_Node_List.remove(node)
        
    def disconnect_From_All_Nodes(self):
        for node in self.connected_Node_List:
            node.connected_Node_List.remove(self)
        self.connected_Node_List.clear()
    
    def get_Connected_Node_List(self) -> list:
        return self.connected_Node_List
        
    def is_Thread_Alive(self) -> bool:
        for thread in self.__thread_list:
            if thread.is_alive():
                return True
        return False

    def get_Data(self) -> object:
        return self.data
    
    def is_Equal_To_Data(self, data) -> bool:
        if self.data == data:
            return True
        else:
            return False
        
    def do_I_Have(self, data):
        if self.is_Equal_To_Data(data):
            return True
        else:
            # Search in connected nodes
            for node in self.connected_Node_List:
                if node.do_I_Have(data):
                    return True
