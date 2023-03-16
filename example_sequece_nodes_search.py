from random import randint, seed
from time import time
from Classes.Container import Container_Struct


def save_to_json(path, data, sort_keys=True, indent=4):
    global json
    import json

    with open(path, "w") as outfile:
        json.dump(data, outfile, sort_keys=sort_keys, indent=indent)
    return 0


print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 1000

seed(time())
SEARCHED_DATA = -13 # randint(0, 100)
NODE_LENGTH = 6  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_LENGTH - randint(1, NODE_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_LENGTH node layers
node_layer_1 = container.create_Node(int(NODE_LENGTH/2))
node_layer_3 = container.create_Node(NODE_LENGTH*2)
node_layer_4 = container.create_Node(NODE_LENGTH)
node_layer_2 = container.create_Node(NODE_LENGTH)
node_layer_5 = container.create_Node(40)
node_layer_last = container.create_Node(NODE_LENGTH)

layer_list = [
    node_layer_1, 
    node_layer_3, 
    node_layer_4, 
    node_layer_2,
    node_layer_5,
    node_layer_last
]

# Connect the first node to the input gate
counter_connections_ordered = container.connect_Node_As_Ordered()

print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())

for layer in layer_list:
    print("Layer Length:", len(layer))

print()
node_layer_last[SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA)
print(
    f"node_layer_last[{SEARCHED_NODE_INDEX}] (id is {node_layer_last[SEARCHED_NODE_INDEX].get_ID()}) contains {node_layer_last[SEARCHED_NODE_INDEX].get_Data()}"
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
for node in result_queue:
    if node is not None:
        print(">{}".format(node.get_ID()), end="")
    else:
        print("None", end="-")
        
print("")

