

# CLASSES

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
# from time import sleep
# from multiprocessing import cpu_count

class Node_Struct(object):
    id_Counter = 0
    # thread_Limit = cpu_count() * 100

    def __init__(self, data=None, connections=None, is_Node_Blocked=False):

        # Self Checker
        if connections is not None:
            if self in connections:
                raise Exception("Node can't be connected to itself")

            # Node Position
            self.connected_Node_List = connections
        else:
            self.connected_Node_List = list()
        
        self.__data = data
        self.__is_Data_Checked = False
        self.checked_by = None
        
        self.__id = self.id_Counter
        
        # Node Block Status
        self.is_Node_Blocked = is_Node_Blocked
        
        # Exit Statement for Threading
        self.exit_Statement = False
        
        # To ensure there will be no rise condition between threads at searching (DO NOT USE DIRECTLY)
        self.__lock = Lock()

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, *args, **kwargs):
        # Node ID
        # cls.id_Counter += 1
        Node_Struct.id_Counter += 1
        return super(Node_Struct, cls).__new__(cls, *args, **kwargs)
    
    def connect_Node_BiDirection(self, node) -> int:
        if type(node) is Node_Struct or type(node) is not list:
            if self is not node:
                self.connected_Node_List.append(node)
                node.connected_Node_List.append(self)
            else:
                raise(Exception("Node can not be connected to itself!"))
        else:
            raise (
                Exception(f"Only Node type is accepted (given {type(node)})!")
            )
        return 2

    def disconnect_Two_Way_Node(self, node) -> int:
        if type(node) is Node_Struct or type(node) is not list:
            self.connected_Node_List.remove(node)
            node.connected_Node_List.remove(self)
        else:
            raise (
                Exception(f"Only Node type is accepted (given {type(node)})!")
            )
        return 2

    def connect_To_Node(self, node) -> int:
        self.connected_Node_List.append(node)
        return 1
        
    def disconnect_From_Node(self, node):
        self.connected_Node_List.remove(node)
        
    def disconnect_From_All_Nodes(self):
        for node in self.connected_Node_List:
            node.connected_Node_List.remove(self)
        self.connected_Node_List.clear()
    
    def get_Connected_Node_List(self) -> list:
        return self.connected_Node_List
        
    def get_Blocked_Status(self):
        return self.is_Node_Blocked
        
    def set_Data(self, data):
        self.__lock.acquire()
        self.__data = data
        self.__lock.release()

    def get_Data(self) -> object:
        return self.__data
    
    def get_ID(self) -> int:
        return self.__id
    
    def compare_Data(self, data) -> bool:
        return self.__data == data
    
    def compare_Data_Aware(self, data) -> list:
        return [self.__data == data, self]
    
    def compare_Multiple_Data_Aware(self, data_list) -> list:
        for data in data_list:
            if data == self.__data:
                return [True, self]
        return [False, self]
    
    def set_Is_Data_Checked(self, bool, checker_node=None):
        self.__is_Data_Checked = bool
        self.checked_by = checker_node
    
    def is_Data_Checked(self):
        return self.__is_Data_Checked
    
    def do_I_Have(self, data, search_history, recursive=True) -> list:
        if self.__data == data:
            search_history.append(self)
            return [self]
        elif recursive:
            result_list = list()
            thread_list = list()
            
            # Search in connected nodes
            with ThreadPoolExecutor(max_workers=None) as executor:  # cpu_count()
                # TODO: Below commented code creates a bug in the program 
                # (it doesn't work) but it should work 
                # (it should limit the number of threads) (it should be fixed) 
                # After a while, the program will stuck because of the 
                # max number of threads are created and not dying
                # while threading.active_count() > Node_Struct.thread_Limit:
                #     sleep(0.1)

                for node in self.connected_Node_List:
                    if node in search_history:
                        continue
                    else:
                        search_history.append(node)
                        thread_list.append(
                                executor.submit(
                                node.do_I_Have,
                                data,
                                search_history
                            )
                        )
                for thread in thread_list:
                    result_list.append(thread.result())
                    
                # Check if there is a result
                for result in result_list:
                    if result != [None]:
                        result.append(self)
                        return result
            return [None]
        else:
            return [None]
        
    def get_Information(self) -> dict:
        return {
            "ID": self.get_ID(),
            "Blocked_Status": self.get_Blocked_Status(),
            "Data": self.get_Data(),
            "Connected_Node_List": self.get_Connected_Node_List(),
        }
        