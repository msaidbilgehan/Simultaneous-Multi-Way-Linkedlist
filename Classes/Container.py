
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread
import sys
from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from Classes.Gate import Gate_Struct, Gate_Point_Cloud_Struct
from Classes.Node import Node_Struct
from Classes.Node_PC import Node_Point_Cloud_Struct, MARKERS, COLORS
from Classes.Search_History import Search_History_List_Struct


class Container_Struct(object):
    id_counter = 0

    def __init__(self, max_workers: int | None = None, do_not_check_again: bool = True, is_point_cloud: bool = False, verbose: bool = False):

        self.id: int = self.id_counter
        self.is_verbose: bool = verbose
        self.__node_List: list[Node_Point_Cloud_Struct | Node_Struct] = list()

        if is_point_cloud:
            self.input_Gate: Gate_Point_Cloud_Struct | Gate_Struct = Gate_Point_Cloud_Struct()
            self.input_Gate.set_Marker(MARKERS.TRIANGLE_UP)
            self.input_Gate.set_Color(COLORS.GREEN)
            self.output_Gate: Gate_Point_Cloud_Struct | Gate_Struct = Gate_Point_Cloud_Struct()
            self.output_Gate.set_Marker(MARKERS.TRIANGLE_DOWN)
            self.output_Gate.set_Color(COLORS.RED)
        else:
            self.input_Gate: Gate_Point_Cloud_Struct | Gate_Struct = Gate_Struct()
            self.output_Gate = Gate_Struct()
        self.__node_List.append(self.input_Gate)
        self.__node_List.append(self.output_Gate)

        self.__node_array_map: list[list[Node_Point_Cloud_Struct | Node_Struct]] = list(
        )
        self.__node_id_array_map: list[list[int]] = list()
        
        self.__search_History: Search_History_List_Struct = Search_History_List_Struct()
        self.__search_Data_List: list = list()
        self.__found_Node_List: list[Node_Point_Cloud_Struct | Node_Struct] = list()
        self.__result_thread_list: list[Future] = list()
        self.__waiting_Node_Cache: list[dict[str, Node_Point_Cloud_Struct | Node_Struct]] = list()
        
        self.__max_Workers: int | None = max_workers
        self.__search_Thread_Active: bool = True
        self.do_not_check_again: bool = do_not_check_again

        self.is_Searched_All_Nodes: bool = False
        self.is_Received_All_Results: bool = False
        
        self.__search_Producer_Thread: Thread
        self.__search_Task_Consumer_Thread: Thread

    # https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
    def __new__(cls, max_workers: int | None = None, do_not_check_again: bool = True, is_point_cloud: bool = False, verbose: bool = False, *args, **kwargs):
        # Node ID
        # cls.id_counter += 1
        Container_Struct.id_counter += 1
        return super(Container_Struct, cls).__new__(cls, *args, **kwargs)
    
    def set_Max_Workers(self, max_Workers: int | None):
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
    
    def create_Node(self, number:int=1, is_point_cloud:bool=False) -> list[Node_Point_Cloud_Struct | Node_Struct]:
        node_list: list = list()
        for _ in range(number):
            node: Node_Point_Cloud_Struct | Node_Struct = Node_Point_Cloud_Struct(
            ) if is_point_cloud else Node_Struct()
            node_list.append(node)
        self.__node_List += node_list
        return node_list
    
    def connect_to_Input_Gate(self, index) -> int:
        self.input_Gate.connect_To_Node(self.__node_List[index])
        return 1
    
    def connect_to_Output_Gate(self, index) -> int:
        self.__node_List[index].connect_To_Node(self.output_Gate)
        return 1

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
        
    @staticmethod
    def connect_Nodes_As_Sequential(nodes, bi_direction=True) -> int:
        connection = 0
        for i in range(len(nodes) - 1):
            if bi_direction:
                connection += nodes[i].connect_Node_BiDirection(nodes[i+1])
            else:
                connection += nodes[i].connect_To_Node(nodes[i+1])
        return connection

    @staticmethod
    def connect_Nodes_One_O_One(layer_1, layer_2, bi_direction=True) -> int:
        connections = 0
        for i in range(len(layer_1)):
            if bi_direction:
                connections += layer_1[i].connect_Node_BiDirection(
                    layer_2[i]
                )
            else:
                connections += layer_1[i].connect_To_Node(
                    layer_2[i]
                )
        return connections

    @staticmethod
    def connect_Nodes_To_Node(from_nodes, to_node, bi_direction=True) -> int:
        connections = 0
        for node in from_nodes:
            if bi_direction:
                connections += node.connect_Node_BiDirection(
                    to_node
                )
            else:
                connections += node.connect_To_Node(
                    to_node
                )
        return connections

    @staticmethod
    def connect_Node_To_Nodes(from_node, to_nodes, bi_direction=True) -> int:
        connections = 0
        for node in to_nodes:
            if bi_direction:
                connections += from_node.connect_Node_BiDirection(
                    node
                )
            else:
                connections += from_node.connect_To_Node(
                    node
                )
        return connections

    def connect_Node_As_Ordered(self) -> int:
        counter_connections = 0
        if len(self.__node_List) > 2:
            counter_connections += self.connect_to_Input_Gate(2)
            counter_connections += self.connect_to_Output_Gate(
                len(self.__node_List) - 1
            )
            # debug_node = None
            for i in range(2, len(self.__node_List) - 1):
                # print(i, self.__node_List[i].get_ID())
                self.__node_List[i].connect_To_Node(self.__node_List[i + 1])
                counter_connections += 1
                # debug_node = self.__node_List[i]
            return counter_connections
        else:
            raise Exception("Node number must be greater than 2")
            return 0

    def create_Node_Map(self, node_layers: list[list[Node_Point_Cloud_Struct | Node_Struct]]):
        self.__node_array_map.append([self.input_Gate])
        for node_layer in node_layers:
            self.__node_array_map.append(node_layer)
        self.__node_array_map.append([self.output_Gate])

    def create_Node_ID_Map(self, node_layers):
        self.__node_id_array_map.append([self.input_Gate.get_ID()])
        for node_layer in node_layers:
            self.__node_id_array_map.append(
                [node.get_ID() for node in node_layer])
        self.__node_id_array_map.append([self.output_Gate.get_ID()])

    def get_Node_Map(self) -> list[list[Node_Point_Cloud_Struct | Node_Struct]]:
        return self.__node_array_map

    def get_Node_ID_Map(self) -> list[list[int]]:
        return self.__node_id_array_map

    def get_Input_Gate(self) -> Gate_Struct | Gate_Point_Cloud_Struct:
        return self.input_Gate
    
    def get_Output_Gate(self) -> Gate_Struct | Gate_Point_Cloud_Struct:
        return self.output_Gate

    def get_Node_List(self) -> list[Node_Point_Cloud_Struct | Node_Struct]:
        return self.__node_List

    def get_Struct(self) -> tuple[list[Node_Point_Cloud_Struct | Node_Struct], Gate_Struct | Gate_Point_Cloud_Struct, Gate_Struct | Gate_Point_Cloud_Struct]:
        return self.get_Node_List(), self.get_Input_Gate(), self.get_Output_Gate()

    def get_Node_Number(self) -> int:
        return len(self.__node_List)

    def get_Connection_Number(self) -> int:
        connection = 0
        for node in self.__node_List:
            connection += len(node.get_Connected_Node_List())
        return connection

    def get_Blocked_Node_Number(self) -> int:
        blocked_Node_Number = 0
        for node in self.__node_List:
            if node.get_Blocked_Status():
                blocked_Node_Number += 1
        return blocked_Node_Number

    def clean_Checked_Status(self):
        for node in self.__node_List:
            node.set_Is_Data_Checked(False)

    def __set_search_Thread_Active(self, bool: bool):
        self.__search_Thread_Active = bool
        
    def __get_search_Thread_Active(self) -> bool:
        return self.__search_Thread_Active

    def __search_Task_Producer(self, waiting_node_cache: list[dict[str, Node_Point_Cloud_Struct | Node_Struct]]):
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

                # DEBUG #
                # print("node.ID:", node.get_ID())
                if node.get_ID() == 4:
                    pass
                #########
                
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
        self.__found_Node_List: list[Node_Point_Cloud_Struct | Node_Struct] = list()
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
                result = thread.result()
                if result != [None]:
                    result_list.append(thread.result())
                
            # result_list = [
            #     result for result_list 
            #     in result_list 
            #     if result != [None] else pass
            # ]
                
        return result_list

    def get_Search_History(self):
        return self.__search_History

    def get_Unconnected_Nodes(self) -> list:
        unconnected_Nodes = list()
        for node in self.__node_List:
            if len(node.get_Connected_Node_List()) == 0:
                unconnected_Nodes.append(node)
        return unconnected_Nodes
    
    def set_Coordinate_Bulk(self, node_list:list, start_x:int=0, start_y:int=0, start_z:int=0, x_step:int=1, y_step:int=1, z_step:int=1):
        for node in node_list:
            node.set_Coordinate(start_x, start_y, start_z)
            start_x += x_step
            start_y += y_step
            start_z += z_step
    
    def plot3D(self, draw_connections: bool = True, draw_labels: bool = True, save_gif: bool = False, num_steps: int=100):

        def walk(start_pos=(0, 0, 0), end_pos=(0, 0, 0), num_steps=100):
            steps = np.linspace(start_pos, end_pos, num_steps)
            # walk = start_pos + np.cumsum(steps, axis=0)
            # walk = np.array([start_pos + step for step in steps], dtype=np.float64)
            walk = np.array(steps, dtype=np.float64)
            return walk

        def update_lines(num, walks, lines):
            for line, walk in zip(lines, walks):
                # NOTE: there is no .set_data() for 3 dim data...
                line.set_data(walk[:num, :2].T)
                line.set_3d_properties(walk[:num, 2])
            return lines

        # https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab

        # TODO: Type Check
        # if not all(isinstance(n, Node_Point_Cloud_Struct) for n in self.__node_List): # Node_Point_Cloud_Struct | Node_Struct
        #     raise Exception("List contains invalid node type!")

        nodes_ID_information = [node.get_ID() for node in self.__node_List]
        nodes_3D_information = [node.get_Information_3D() for node in self.__node_List]
        location_color_marker_data = [
            (node_3D["coordinates"], node_3D["color"], node_3D["marker"])
            for node_3D in nodes_3D_information
        ]
        
        location_data_connected = [
            node_3D["connected_coordinates"]
            for node_3D in nodes_3D_information
        ]

        xdata = [ld[0][0] for ld in location_color_marker_data]
        ydata = [ld[0][1] for ld in location_color_marker_data]
        zdata = [ld[0][2] for ld in location_color_marker_data]
        color_data = [ld[1] for ld in location_color_marker_data]
        marker_data = [ld[2] for ld in location_color_marker_data]

        # Data: walks as arrays
        walks = list()

        for i, ld in enumerate(location_color_marker_data):
            for ldc in location_data_connected[i]:
                walks.append(
                    walk(
                        start_pos=ld[0],
                        end_pos=ldc,
                        num_steps=num_steps
                    )
                )

        # Attaching 3D axis to the figure
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(projection="3d")

        # Create lines initially without data
        lines = [ax.plot([], [], [])[0] for _ in walks]

        # Setting the axes properties
        ax.set(xlim3d=(0, 1), xlabel='X')
        ax.set(ylim3d=(0, 1), ylabel='Y')
        ax.set(zlim3d=(0, 1), zlabel='Z')

        # Creating the Animation object
        if draw_connections:
            anim = animation.FuncAnimation(
                fig,
                update_lines,
                num_steps,
                fargs=(walks, lines),
                interval=100,
                repeat=False
            )

        # Visualize 3D scatter plot
        # ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='jet', s=50)
        # ax.scatter3D(X[Z <= 5], Y[Z <= 5], Z[Z <= 5], s=70, c='g', marker='x')
        for i, ld in enumerate(location_color_marker_data):
            ax.scatter3D(  # type: ignore
                xdata[i], ydata[i], zdata[i],
                c=color_data[i].value,
                marker=marker_data[i].value,
                s=50
            )
        ax.view_init(elev=25, azim=-30)  # type: ignore
        ax.autoscale(enable=True, axis='both', tight=None)

        # Visualize labels
        if draw_labels:
            for i, id in enumerate(nodes_ID_information):
                ax.text(xdata[i], ydata[i], zdata[i], id, color='red')

        # Visualize Connections
        # for i, ld_connected_nodes in enumerate(location_data_connected):
        #     for ld_connected in ld_connected_nodes:
        #         x_line = np.linspace(xdata[i], ld_connected[0], 2)
        #         y_line = np.linspace(ydata[i], ld_connected[1], 2)
        #         z_line = np.linspace(zdata[i], ld_connected[2], 2)
        #         ax.plot3D(x_line, y_line, z_line, 'blue')

        # Give labels
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')  # type: ignore

        # Save figure
        plt.show()
        # plt.savefig('3d_scatter.png', dpi=300)
        
        if save_gif and draw_connections:
            writer_gif = animation.PillowWriter(fps=30)
            anim.save(r"animation.gif", writer=writer_gif) # type: ignore
        else:
            plt.savefig('3D_Node_Map.png')

    @staticmethod
    def optimize_Path(path: list[Node_Point_Cloud_Struct | Node_Struct], target: Node_Point_Cloud_Struct | Node_Struct) -> list[Node_Point_Cloud_Struct | Node_Struct]:
        # print(f"Before Path ({len(path)}):", [node.get_ID() for node in path])

        original_path = path.copy()
        while True:
            last_match = None
            removed_counter = 0
            path_start_length = len(path)
            for i, node in enumerate(path):
                connected_nodes = node.get_Connected_Node_List()

                if last_match is not None:
                    path[i] = last_match
                    removed_counter = path_start_length - i
                    if last_match == target:
                        while removed_counter:
                            path.pop()
                            removed_counter -= 1
                        break

                last_match = None

                for local_node in path[i:]:
                    if local_node in connected_nodes:
                        last_match = local_node
            if original_path == path:
                break
            original_path = path.copy()
            path.append(target)

        path.append(target)
        # sorted(set(path), key=lambda node: node.get_ID())
        sorted(path, key=lambda node: node.get_ID())
        # print(f"After Path ({len(path)}):", [node.get_ID() for node in path])
        return path

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
    def find_Path_By_Checker_Node(node, input_Gate: Node_Struct | Node_Point_Cloud_Struct) -> list[Node_Struct | Node_Point_Cloud_Struct]:
        path: list[Node_Struct | Node_Point_Cloud_Struct] = list()
        current_Node = node
        
        while True:
            path.append(current_Node)
            # print(current_Node.get_ID(), end="\r")
            if current_Node is not input_Gate:
                current_Node = current_Node.checked_by
            else:
                path.append(current_Node)
                break
            
        return path

