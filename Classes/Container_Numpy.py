
from Classes.Container import Container_Struct
import numpy as np


class Container_Numpy_Struct(Container_Struct):
    id_counter = 0

    def __init__(self, max_workers:int|None=None, do_not_check_again:bool=True, verbose:bool=False):
        super().__init__(
            max_workers,
            do_not_check_again, 
            verbose
        )
        self.__node_id_data_numpy_map = np.array([])

    def create_Node_ID_Numpy_Mapping(self):
        self.__node_id_data_numpy_map = np.array(
            [[node.get_ID(), node.get_Data()] for node in self.get_Struct()[0]]
        )

    def get_Numpy_Mapping(self):
        return self.__node_id_data_numpy_map
    
    def contains_Numpy(self, id: int = -1, data=None) -> tuple:
        if id != -1 and data is None:
            return np.where(self.__node_id_data_numpy_map[:, 0] == id)
        elif id == -1 and data is not None:
            return np.where(self.__node_id_data_numpy_map[:, 1] == data)
        elif id != -1 and data is not None:
            return np.where(self.__node_id_data_numpy_map[:, :] == (id, data))
        else:
            return ()

    def create_Node_Data_Numpy_Mapping(self):
        self.__node_id_data_numpy_map = np.array(
            [node.id for node in self.__node_List]
        )
