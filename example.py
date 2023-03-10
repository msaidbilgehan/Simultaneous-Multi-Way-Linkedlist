import os
from random import randint, seed
from time import time
from Classes.Container import Container_Struct
# from multiprocessing import cpu_count


def path_control(path, is_file=True, is_directory=True):
    bool_list = list()
    if is_file:
        bool_list.append(os.path.isfile(path))
    if is_directory:
        bool_list.append(os.path.isdir(path))
    return bool_list

def save_to_json(path, data, sort_keys=True, indent=4):
    global json
    import json

    with open(path, "w") as outfile:
        json.dump(data, outfile, sort_keys=sort_keys, indent=indent)
    return 0

def load_from_json(path):
    data = None
    if path_control(path, is_file=True)[0]:
        global json
        import json

        with open(path, "r") as json_file:
            data = json.load(json_file)
    return data

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 1000

seed(time())
SEARCHED_DATA = -13 # randint(0, 100)
NODE_LENGTH = 400  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_LENGTH - randint(1, NODE_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_LENGTH node layers
node_layer_1 = container.create_Node(int(NODE_LENGTH/2))
node_layer_2 = container.create_Node(NODE_LENGTH)
node_layer_3 = container.create_Node(NODE_LENGTH*2)
node_layer_4 = container.create_Node(NODE_LENGTH)
node_layer_last = container.create_Node(NODE_LENGTH)

layer_list = [
    node_layer_1, 
    node_layer_2,
    node_layer_3, 
    node_layer_4, 
    node_layer_last
]
# container.create_Node_ID_Map(
#     node_layers=layer_list
# )
# node_ID_Map = container.get_Node_ID_Map()
# print(node_ID_Map)
# save_to_json("node_ID_Map.json", node_ID_Map, sort_keys=False, indent=4)

counter_connections = 0
counter_connections += container.connect_Input_Gate_to_Node_Layer(node_layer_1)
counter_connections += container.connect_Node_Layers(node_layer_1, node_layer_2)
counter_connections += container.connect_Node_Layers(node_layer_2, node_layer_3)
counter_connections += container.connect_Node_Layers(node_layer_3, node_layer_4)
counter_connections += container.connect_Node_Layers(node_layer_4, node_layer_last)
counter_connections += container.connect_Node_Layer_To_Output_Gate(node_layer_3)

# Connect the first node to the input gate
# counter_connections_ordered = container.connect_Node_As_Ordered()

print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())
print("Connections:", counter_connections)

for layer in layer_list:
    print("Layer Length:", len(layer))

print()
node_layer_last[SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA)
print(
    f"node_layer_last[{SEARCHED_NODE_INDEX}] (id is {node_layer_last[SEARCHED_NODE_INDEX].id}) contains {node_layer_last[SEARCHED_NODE_INDEX].get_Data()}"
)
print(f"Looking for data: {SEARCHED_DATA}")

print("===== Sequential Search =====")
# get the start time
start_time = time()
result_queue = container.search(SEARCHED_DATA)
end_time = time()

elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

# print("Result Queue:", result_queue)
print()

print("Path Length:", len(result_queue))
# for node in result_queue:
#     if node is not None:
#         print(">{}".format(node.id), end="-")
#     else:
#         print("None", end="-")


print("===== Multi-Threaded Search =====")

start_time = time()
found_node_list = container.search_Task(SEARCHED_DATA, True, True)
end_time = time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

print(f"Found {len(found_node_list)} different Node Path")

# if len(found_node_list) > 0:
#     print("found_node_list:", found_node_list[-1].id, found_node_list)
    
print("")
