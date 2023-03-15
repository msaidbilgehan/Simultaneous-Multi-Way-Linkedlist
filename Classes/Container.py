
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import sys
from time import sleep
from Classes.Gate import Gate_Struct
from Classes.Node import Node_Struct
from Classes.Search_History import Search_History_List_Struct


class Container_Struct(object):
    id_counter = 0

    def __init__(self, max_workers:int|None=None, do_not_check_again:bool=True, verbose:bool=False):

        self.id = self.id_counter
        self.is_verbose = verbose
        
        self.input_Gate = Gate_Struct()
        self.output_Gate = Gate_Struct()
        
        self.__node_array_map = list()
        self.__node_id_array_map = list()
        
        self.__node_List = list()
        self.__search_History = Search_History_List_Struct()
        self.__search_Data_List = list()
        self.__found_Node_List = list()
        self.__result_thread_list = list()
        self.__waiting_Node_Cache = list()
        
        self.__max_Workers = max_workers
        self.__search_Thread_Active = True
        self.do_not_check_again = do_not_check_again

        self.is_Searched_All_Nodes = False
        self.is_Received_All_Results = False
        
        self.__search_Producer_Thread = None
        self.__search_Task_Consumer_Thread = None
        
        # self.__search_Producer_Thread = Thread(
        #     target=self.__search_Task_Producer,
        #     args=[
        #         self.__waiting_Node_Cache
        #     ]
        # )

        # # don't hang on exit
        # self.__search_Producer_Thread.setDaemon(True)
        # self.__search_Producer_Thread.start()
        
        # self.__search_Task_Consumer_Thread = Thread(
        #     target=self.__search_Task_Consumer,
        #     args=[]
        # )

        # # don't hang on exit
        # self.__search_Task_Consumer_Thread.setDaemon(True)
        # self.__search_Task_Consumer_Thread.start()

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, max_workers: int | None = None, do_not_check_again: bool = True, verbose: bool = False, *args, **kwargs):
        # Node ID
        # cls.id_counter += 1
        Container_Struct.id_counter += 1
        return super(Container_Struct, cls).__new__(cls, *args, **kwargs)
    
    def set_Max_Workers(self, max_Workers):
        self.__max_Workers = max_Workers
        self.restart_Search_Thread()
        
    def restart_Search_Thread(self):
        self.__search_Thread_Active = False
        self.__search_Task_Thread.join()

        self.__search_Task_Thread = Thread(
            target=self.__search_Task_Producer,
            args=[
                self.__waiting_Node_Cache
            ]
        )
        self.__search_Task_Thread.setDaemon(True)  # don't hang on exit
        self.__search_Thread_Active = True

        self.__search_Task_Thread.start()
        
    def get_Max_Workers(self):
        return self.__max_Workers
    
    def create_Node(self, number=1) -> list:
        node_list = list()
        for _ in range(number):
            node = Node_Struct()
            node_list.append(node)
        self.__node_List += node_list
        return node_list
    
    def connect_to_Input_Gate(self, index) -> int:
        self.input_Gate.connect_To_Node(self.__node_List[index])
        return 1
    
    def connect_to_Output_Gate(self, index) -> int:
        self.__node_List[index].connect_To_Node(self.output_Gate)
        return 1

    def create_Node_Map(self, node_layers):
        self.__node_array_map.append([self.input_Gate])
        for node_layer in node_layers:
            self.__node_array_map.append(node_layer)
        self.__node_array_map.append([self.output_Gate])
    
    def create_Node_ID_Map(self, node_layers):
        self.__node_id_array_map.append([self.input_Gate.id])
        for node_layer in node_layers:
            self.__node_id_array_map.append([node.id for node in node_layer])
        self.__node_id_array_map.append([self.output_Gate.id])
    
    def get_Node_Map(self):
        return self.__node_array_map
    
    def get_Node_ID_Map(self):
        return self.__node_id_array_map
    
    def connect_Node_Layers(self, node_layer_1, node_layer_2) -> int:
        counter_connections = 0
        for layer_1_node in node_layer_1:
            for layer_2_node in node_layer_2:
                layer_1_node.connect_To_Node(layer_2_node)
                counter_connections += 1
        return counter_connections

    def connect_Input_Gate_to_Node_Layer(self, node_layer) -> int:
        counter_connections = 0
        for node in node_layer:
            self.input_Gate.connect_To_Node(node)
            counter_connections += 1
        return counter_connections

    def connect_Node_Layer_To_Output_Gate(self, node_layer) -> int:
        counter_connections = 0
        for node in node_layer:
            node.connect_To_Node(self.output_Gate)
            counter_connections += 1
        return counter_connections

    def connect_To_Custom_Node_List(self, node_list, input_Gate_Index, output_Gate_Index):
        counter_connections = 0
        self.__node_List = node_list
        counter_connections += self.connect_to_Input_Gate(input_Gate_Index)
        counter_connections += self.connect_to_Output_Gate(output_Gate_Index)
        return counter_connections
        
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

    @staticmethod
    def connect_Nodes_As_Sequential(nodes, bi_direction=True) -> int:
        connections = 0
        for i in range(len(nodes) - 1):
            nodes[i].connect_To_Node(nodes[i+1])
            connections += 1
            if bi_direction:
                nodes[i+1].connect_To_Node(nodes[i])
                connections += 1
        return connections

    @staticmethod
    def connect_Nodes_One_O_One(layer_1, layer_2, bi_direction=True) -> int:
        connections = 0
        for i in range(len(layer_1)):
            connections += 1
            layer_1[i].connect_To_Node(
                layer_2[i]
            )
            if bi_direction:
                layer_2[i].connect_To_Node(
                    layer_1[i]
                )
                connections += 1
        return connections

    @staticmethod
    def connect_Nodes_To_Node(from_nodes, to_node, bi_direction=True) -> int:
        connections = 0
        for node in from_nodes:
            node.connect_To_Node(
                to_node
            )
            connections += 1
            if bi_direction:
                to_node.connect_To_Node(
                    node
                )
                connections += 1
        return connections

    @staticmethod
    def connect_Node_To_Nodes(from_node, to_nodes, bi_direction=True) -> int:
        connections = 0
        for node in to_nodes:
            node.connect_To_Node(
                from_node
            )
            connections += 1
            if bi_direction:
                from_node.connect_To_Node(
                    node
                )
                connections += 1
        return connections

    def connect_Node_As_Ordered(self) -> int:
        counter_connections = 0
        if len(self.__node_List) > 2:
            counter_connections += self.connect_to_Input_Gate(0)
            counter_connections += self.connect_to_Output_Gate(
                len(self.__node_List) - 1
            )
            # debug_node = None
            for i in range(0, len(self.__node_List) - 1):
                # print(i, self.__node_List[i].id)
                self.__node_List[i].connect_To_Node(self.__node_List[i + 1])
                counter_connections += 1
                # debug_node = self.__node_List[i]
            return counter_connections
        else:
            raise Exception("Node number must be greater than 2")
            return 0

    def clean_Checked_Status(self):
        for node in self.__node_List:
            node.set_Is_Data_Checked(False)

    def __set_search_Thread_Active(self, bool: bool):
        self.__search_Thread_Active = bool
        
    def __get_search_Thread_Active(self):
        return self.__search_Thread_Active

    def __search_Task_Producer(self, waiting_node_cache):
        __total_Checked_Node = 0

        while self.__search_Thread_Active:
            # Check if there is a new thread in waiting thread cache
            with ThreadPoolExecutor(max_workers=self.get_Max_Workers()) as executor:
                # Search in connected nodes
                while self.__search_Thread_Active:
                    if len(waiting_node_cache) > 0:
                        node_pack = waiting_node_cache.pop()
                    else:
                        continue
                    
                    parent_node, child_node = node_pack.values()

                    if child_node is None:
                        continue
                    if self.get_Do_Not_Check_Again() and child_node.is_Data_Checked():
                        continue

                    # Start a thread for each node
                    self.__result_thread_list.append(
                        executor.submit(
                            child_node.compare_Multiple_Data_Aware,
                            self.__search_Data_List
                        )
                    )

                    self.__search_History.append(
                        child_node
                    )
                    
                    __total_Checked_Node += 1
                    # if self.is_verbose:
                    #     print(
                    #         f"TOTAL CHECKED NODE: {__total_Checked_Node}",
                    #         end="\r"
                    #     )
                    child_node.set_Is_Data_Checked(True, parent_node)
                    
                    for neighbor in child_node.get_Connected_Node_List():
                        waiting_node_cache.append(
                            {
                                "parent_node": child_node,
                                "child_node": neighbor,
                            }
                        )

                    sleep(0.01)
                    if self.get_Do_Not_Check_Again():
                        if __total_Checked_Node == len(self.__node_List):
                            self.set_Is_Searched_All_Nodes(True)
                            break
                    else:
                        # TODO: If every thread can check the node already checked
                        # How do we know the search run is finished?
                        pass

    def __search_Task_Consumer(self):
        result_list = list()
        found_results = list()
        __total_Checked_Node = 0
        
        while self.__search_Thread_Active:
            # Wait for all threads to finish
            if len(self.__result_thread_list) > 0:                
                result_thread = self.__result_thread_list.pop()
                result_list.append(result_thread.result())
                # Check if there is a result
                result, node = result_list[-1]
                __total_Checked_Node += 1
                if self.is_verbose:
                    print(
                        f"Getting Result From Nodes: {__total_Checked_Node}",
                        end="\r"
                    )
                if result:
                    found_results.append(node)
                    self.__found_Node_List.append(node)

                if self.get_Do_Not_Check_Again():
                    if __total_Checked_Node == len(self.__node_List):
                        if self.is_verbose:
                            print()
                        self.set_Is_Received_All_Results(True)
                        break
                    else:
                        # TODO: If every thread can check the node already checked
                        # How do we know the search run is finished?
                        pass

    def set_Do_Not_Check_Again(self, bool):
        self.do_not_check_again = bool
        
    def get_Do_Not_Check_Again(self):
        return self.do_not_check_again

    def get_Is_Searched_All_Nodes(self) -> bool:
        return self.is_Searched_All_Nodes
    
    def set_Is_Searched_All_Nodes(self, bool):
        self.is_Searched_All_Nodes = bool

    def get_Is_Received_All_Results(self) -> bool:
        return self.is_Received_All_Results

    def set_Is_Received_All_Results(self, bool):
        self.is_Received_All_Results = bool

    def search_Task(self, data:list, wait_until_k_number_found:int=-1, do_not_check_again:bool=True):
        self.__search_Data_List = data
        self.__found_Node_List = list()
        self.set_Do_Not_Check_Again(do_not_check_again)
        
        self.__set_search_Thread_Active(True)
        
        self.__search_Producer_Thread = Thread(
            target=self.__search_Task_Producer,
            args=[
                self.__waiting_Node_Cache
            ]
        )

        # don't hang on exit
        self.__search_Producer_Thread.setDaemon(True)
        self.__search_Producer_Thread.start()

        self.__search_Task_Consumer_Thread = Thread(
            target=self.__search_Task_Consumer,
            args=[]
        )

        # don't hang on exit
        self.__search_Task_Consumer_Thread.setDaemon(True)
        self.__search_Task_Consumer_Thread.start()
        
        # Search in connected nodes (input gate)
        self.__waiting_Node_Cache.append(
            {
                "parent_node": self.input_Gate,
                "child_node": self.input_Gate,
            }
        )
        
        # Wait until search process to finish or k number found 
        while not self.is_Received_All_Results:
            if len(self.__found_Node_List) >= wait_until_k_number_found and wait_until_k_number_found > 0:
                break
            
            if self.get_Do_Not_Check_Again():
                if self.get_Is_Searched_All_Nodes():
                    if self.is_verbose:
                        print("Searched all nodes!")
                    self.set_Is_Searched_All_Nodes(False)
                elif self.get_Is_Received_All_Results():
                    if self.is_verbose:
                        print("Received all nodes!")
                    self.set_Is_Received_All_Results(False)
                    break
            else:
                # TODO: If every thread can check the node already checked
                # How do we know the search run is finished?
                pass
        
        self.__set_search_Thread_Active(False)
        return self.__found_Node_List

    def search(self, data):
        # Create a list to store all threads
        thread_list = list()
        result_list = list()
        search_history = Search_History_List_Struct()
        
        with ThreadPoolExecutor(max_workers=self.get_Max_Workers()) as executor:
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

    def get_Search_History(self):
        return self.__search_History
    
    @staticmethod
    def set_Recursion_Limit(value:int=10000):
        sys.setrecursionlimit(value)

    @staticmethod
    def get_Recursion_Limit():
        return sys.getrecursionlimit()

    @staticmethod
    def find_Path_By_Checker_Node_Recursive(node, input_Gate) -> list:
        path = list()
        if node[0] is not input_Gate:
            path += Container_Struct.find_Path_By_Checker_Node_Recursive(
                [node[0].checked_by], 
                input_Gate
            )
            path.append(node[0])
            return path
        else:
            return [input_Gate]

    @staticmethod
    def find_Path_By_Checker_Node(node, input_Gate) -> list:
        path = list()
        current_Node = node
        
        while True:
            path.append(current_Node)
            # print(current_Node.id, end="\r")
            if current_Node is not input_Gate:
                current_Node = current_Node.checked_by
            else:
                path.append(current_Node)
                break
        return path
