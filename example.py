from random import randint, seed
from time import time
from Classes.Container import Container_Struct
# from multiprocessing import cpu_count


def save_to_json(path, data, sort_keys=True, indent=4):
    global json
    import json

    with open(path, "w") as outfile:
        json.dump(data, outfile, sort_keys=sort_keys, indent=indent)
    return 0


print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

seed(time())

SEARCHED_DATA_1 = -13  # randint(0, 100)
SEARCHED_DATA_2 = 73  # randint(0, 100)

NODE_LENGTH = 5  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_LENGTH - randint(1, NODE_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS, verbose=True)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_LENGTH node layers
node_layer_1 = container.create_Node(NODE_LENGTH)
node_layer_3 = container.create_Node(NODE_LENGTH)
node_layer_4 = container.create_Node(NODE_LENGTH)
node_layer_2 = container.create_Node(NODE_LENGTH)
node_layer_6 = container.create_Node(NODE_LENGTH)
node_layer_7 = container.create_Node(NODE_LENGTH)
node_layer_5 = container.create_Node(25)
node_layer_last = container.create_Node(NODE_LENGTH)

layer_list = [
    node_layer_1,
    node_layer_3,
    node_layer_4,
    node_layer_2,
    node_layer_6,
    node_layer_7,
    node_layer_5,
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
counter_connections += container.connect_Node_Layers(
    node_layer_1, node_layer_4
)
counter_connections += container.connect_Node_Layers(
    node_layer_4, node_layer_2
)
counter_connections += container.connect_Node_Layers(
    node_layer_2, node_layer_3
)
counter_connections += container.connect_Node_Layers(
    node_layer_3, node_layer_6
)
counter_connections += container.connect_Node_Layers(
    node_layer_6, node_layer_7
)
counter_connections += container.connect_Node_Layers(
    node_layer_7, node_layer_5
)
counter_connections += container.connect_Node_Layers(
    node_layer_5, node_layer_last
)
counter_connections += container.connect_Node_Layer_To_Output_Gate(
    node_layer_last
)

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

node_layer_last[SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA_1)
print(
    f"node_layer_last[{SEARCHED_NODE_INDEX}] (id is {node_layer_last[SEARCHED_NODE_INDEX].id}) contains {node_layer_last[SEARCHED_NODE_INDEX].get_Data()}"
)
node_layer_7[len(node_layer_7) - 5].set_Data(SEARCHED_DATA_1)
print(
    f"node_layer_7[{len(node_layer_7) - 5}] (id is {node_layer_7[len(node_layer_7) - 5].id}) contains {node_layer_7[len(node_layer_7) - 5].get_Data()}"
)
node_layer_1[len(node_layer_1) - 3].set_Data(SEARCHED_DATA_2)
print(
    f"node_layer_1[{len(node_layer_1) - 3}] (id is {node_layer_1[len(node_layer_1) - 3].id}) contains {node_layer_1[len(node_layer_1) - 3].get_Data()}"
)
print(f"Looking for data: {SEARCHED_DATA_1, SEARCHED_DATA_2}")

print("")
print("===== Multi-Threaded Search =====")

start_time = time()
# data, wait_until_k_number_found=-1, do_not_check_again=True
found_node_list = container.search_Task(
    [SEARCHED_DATA_1, SEARCHED_DATA_2], 
    -1, 
    True
)
end_time = time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

print(f"Found {len(found_node_list)} Node")
print("IDs:", [node.id for node in found_node_list])

_, input_gate, _ = container.get_Struct()
for found_node in found_node_list:
    path_checker_result = container.find_Path_By_Checker_Node(
        found_node,
        input_gate
    )
    path_checker_result = path_checker_result[:-1]
    path_checker_result = path_checker_result[::-1]
    print("")
    print("Find Path by Checker Result:")
    for step in path_checker_result:
        print(step.id, end=" > ")

    print("path length:", len(path_checker_result))

# for index, history in enumerate(search_history):
#     # Pass input gate
#     if index == 0:
#         continue
#     print(
#         index,
#         "|",
#         history["parent_node"].id,
#         history["child_node"].id,
#         "\t|",
#         history["parent_node_index"],
#         "  \t|",
#         history["result"],
#     )

container.clean_Checked_Status()

print("")
