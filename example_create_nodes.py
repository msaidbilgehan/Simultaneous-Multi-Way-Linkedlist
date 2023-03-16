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

seed(time())
SEARCHED_DATA = -13 # randint(0, 100)
NODE_LENGTH = 10  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_LENGTH - randint(1, NODE_LENGTH-1)

# Create a container
container = Container_Struct()

print()
print("=== Create Nodes ===")
# Create NODE_LENGTH node layers
node_pack_1 = container.create_Node(int(NODE_LENGTH/2))
node_pack_3 = container.create_Node(NODE_LENGTH*2)
node_pack_4 = container.create_Node(NODE_LENGTH)
node_pack_2 = container.create_Node(NODE_LENGTH)
node_pack_5 = container.create_Node(40)
node_pack_last = container.create_Node(NODE_LENGTH)

layer_list = [
    node_pack_1, 
    node_pack_3, 
    node_pack_4, 
    node_pack_2,
    node_pack_5,
    node_pack_last
]
container.create_Node_ID_Map(
    node_layers=layer_list
)
node_ID_Map = container.get_Node_ID_Map()
print(node_ID_Map)
save_to_json("node_ID_Map.json", node_ID_Map, sort_keys=False, indent=4)

# Connect the first node to the input gate
counter_connections_ordered = container.connect_Node_As_Ordered()

print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())

print()
node_pack_last[SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA)
print(
    f"node_pack_last[{SEARCHED_NODE_INDEX}] (id is {node_pack_last[SEARCHED_NODE_INDEX].get_ID()}) contains {node_pack_last[SEARCHED_NODE_INDEX].get_Data()}"
)
