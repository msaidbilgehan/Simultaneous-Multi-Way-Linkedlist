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
number_of_max_worker = 100

seed(time())
searched_data = -13 # randint(0, 100)
node_length = 3  # randint(0, 10000) or cpu_count() * 100
search_node_index = node_length - randint(1, node_length-1)

# Create a container
container = Container_Struct(number_of_max_worker)
# container.set_Max_Workers(number_of_max_worker)

print("Max Workers:", container.get_Max_Workers())

# Create node_length node layers
node_layer_1 = container.create_Node(int(node_length/2))
node_layer_2 = container.create_Node(node_length)
node_layer_3 = container.create_Node(node_length*2)
node_layer_4 = container.create_Node(node_length)
node_layer_last = container.create_Node(node_length)

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
node_layer_last[search_node_index].set_Data(searched_data)
print(
    f"node_layer_last[{search_node_index}] (id is {node_layer_last[search_node_index].id}) contains {node_layer_last[search_node_index].get_Data()}"
)
print(f"Looking for data: {searched_data}")

print("===== Sequential Search =====")
# get the start time
start_time = time()
result_queue = container.search(searched_data)
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
found_node_list = container.search_Task(searched_data)
end_time = time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

print(f"Found {len(found_node_list)} different Node Path")

# if len(found_node_list) > 0:
#     print("found_node_list:", found_node_list[-1].id, found_node_list)
    
print("")
