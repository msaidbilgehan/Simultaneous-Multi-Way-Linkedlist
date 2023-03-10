
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
from Classes.Gate import Gate_Struct
from Classes.Node import Node_Struct
from Classes.Search_History import Search_History_List_Struct


class Container_Struct(object):
    id_counter = 0

    def __init__(self):

        self.id = self.id_counter
        
        self.input_Gate = Gate_Struct()
        self.output_Gate = Gate_Struct()
        
        self.__node_List = list()
        self.__search_History = Search_History_List_Struct()
        self.__search_Data = None
        self.__found_Node_List = list()
        self.__waiting_Node_Cache = list()
        self.__max_Workers = None
        # self.__active_Thread_Cache = list()
        self.__search_Producer_Thread = Thread(
            target=self.__search_Producer_Task,
            args=[
                self.__waiting_Node_Cache
            ]
        )
        self.__search_Producer_Thread.setDaemon(True)  # don't hang on exit
        self.__search_Producer_Thread.start()
        # self.__search_Consumer_Thread = Thread(
        #     target=self.__search_Consumer_Task,
        #     args=[
        #         self.__active_Thread_Cache
        #     ]
        # )
        # self.__search_Consumer_Thread.start()

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, *args, **kwargs):
        # Node ID
        # cls.id_counter += 1
        Container_Struct.id_counter += 1
        return super(Container_Struct, cls).__new__(cls, *args, **kwargs)
    
    def set_Max_Workers(self, max_Workers):
        self.__max_Workers = max_Workers
        
    def get_Max_Workers(self):
        return self.__max_Workers
    
    def create_Node(self, number=1) -> list:
        node_list = list()
        for _ in range(number):
            node = Node_Struct()
            node_list.append(node)
        self.__node_List += node_list
        return node_list
    
    def connect_to_Input_Gate(self, index):
        self.input_Gate.connect_To_Node(self.__node_List[index])
    
    def connect_to_Output_Gate(self, index):
        self.__node_List[index].connect_To_Node(self.output_Gate)

    def connect_Node_Layers(self, node_layer_1, node_layer_2):
        for layer_1_node in node_layer_1:
            for layer_2_node in node_layer_2:
                layer_1_node.connect_To_Node(layer_2_node)

    def connect_Input_Gate_to_Node_Layer(self, node_layer):
        for node in node_layer:
            self.input_Gate.connect_To_Node(node)

    def connect_Node_Layer_To_Output_Gate(self, node_layer):
        for node in node_layer:
            node.connect_To_Node(self.output_Gate)

    def connect_To_Custom_Node_List(self, node_list, input_Gate_Index, output_Gate_Index):
        self.__node_List = node_list
        self.connect_to_Input_Gate(input_Gate_Index)
        self.connect_to_Output_Gate(output_Gate_Index)
        
    def get_Struct(self):
        return self.__node_List, self.input_Gate, self.output_Gate
    
    def get_Node_Number(self):
        return len(self.__node_List)
    
    def get_Blocked_Node_Number(self):
        blocked_Node_Number = 0
        for node in self.__node_List:
            if node.get_Blocked_Status():
                blocked_Node_Number += 1
        return blocked_Node_Number
    
    def connect_Node_As_Ordered(self):
        if len(self.__node_List) > 2:
            self.connect_to_Input_Gate(0)
            self.connect_to_Output_Gate(len(self.__node_List) - 1)
            # debug_node = None
            for i in range(0, len(self.__node_List) - 1):
                # print(i, self.__node_List[i].id)
                self.__node_List[i].connect_To_Node(self.__node_List[i + 1])
                # debug_node = self.__node_List[i]
        else:
            raise Exception("Node number must be greater than 2")

    def __search_Producer_Task(self, waiting_node_cache):
        while True:
            result_list = list()
            
            # Check if there is a new thread in waiting thread cache
            # if len(waiting_node_cache):
            #     print("waiting_node_cache last id", waiting_node_cache[-1][-1].id, "LEN:", len(waiting_node_cache))
            with ThreadPoolExecutor(max_workers=self.__max_Workers) as executor:
                # Search in connected nodes
                while True:
                    local_waiting_node_cache = list()
                    local_thread_list = list()

                    for caller_node, waiting_node in waiting_node_cache:
                        # print("waiting_node_cache", len(waiting_node_cache))
                        
                        if waiting_node is None:
                            continue
                        
                        # node_path.append(waiting_node)
                        self.__search_History.append([caller_node, waiting_node])
                        
                        # Start a thread for each node
                        local_thread_list.append(
                            executor.submit(
                                waiting_node.compare_Data_Aware,
                                self.__search_Data
                            )
                        )

                    # Wait for all threads to finish
                    for thread in local_thread_list:
                        result_list.append(thread.result())
                        
                        # Check if there is a result
                        result, node = result_list[-1]
                        if result:
                            self.__found_Node_List.append(node)
                            local_waiting_node_cache.append(
                                [node, None]
                            )
                        else:
                            for neighbor in node.get_Connected_Node_List():
                                local_waiting_node_cache.append(
                                    [node, neighbor]
                                )
                    
                    waiting_node_cache.clear()
                    waiting_node_cache += local_waiting_node_cache
                    
                    sleep(0.01)

    # def __search_Consumer_Task(self, active_thread_cache):
    #     while True:
    #         # Check if there is a new thread in active thread cache
    #         for active_thread in active_thread_cache:
    #             active_thread.join()
    #             sleep(0.1)
    #         sleep(0.1)

    def search_Task(self, data, wait_For_First_Output_Gate=True):
        self.__search_Data = data
        self.__search_History = list()
        self.__found_Node_List = list()
        # self.__search_History[self.input_Gate] = dict()
        
        # Search in connected nodes (input gate)
        self.__waiting_Node_Cache.append(
            [self.input_Gate, self.input_Gate]
        )
        # for node in self.input_Gate.get_Connected_Node_List():
        #     # Start a thread for each node
        #     self.__waiting_Node_Cache.append(
        #         [self.input_Gate, node]
        #     )
        
        # TODO: How to understand all search tasks completed?
        
        while wait_For_First_Output_Gate:
            if len(self.__found_Node_List) > 0:
                return self.__found_Node_List
        return self.__found_Node_List

    def search(self, data):
        # Create a list to store all threads
        thread_list = list()
        result_list = list()
        search_history = Search_History_List_Struct()
        
        with ThreadPoolExecutor(max_workers=None) as executor:
            # Search in connected nodes
            for node in self.input_Gate.get_Connected_Node_List():
                # Start a thread for each node
                thread_list.append(
                    executor.submit(
                        node.do_I_Have,
                        data,
                        search_history,
                        True
                    )
                )
                
            # Wait for all threads to finish
            for thread in thread_list:
                result_list.append(thread.result())
                
            # Check if there is a result
            for result in result_list:
                if result != [None]:
                    result.append(self)
                    return result
                
        return [None]
