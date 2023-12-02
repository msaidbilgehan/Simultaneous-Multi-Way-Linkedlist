from time import time
from Classes.Container import Container_Struct
import secrets

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

secrets.SystemRandom().seed(time())
SEARCHED_DATA = -13  # randint(0, 100)
NODE_COLUMN_LENGTH = 10  # randint(0, 10000) or cpu_count() * 100
NODE_ROW_LENGTH = 10  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_COLUMN_LENGTH - secrets.SystemRandom().randint(1, NODE_COLUMN_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_COLUMN_LENGTH x NODE_ROW_LENGTH node layers
node_layer_list = list()
counter_connections = 0
for i in range(NODE_ROW_LENGTH):
    node_layer_list.append(container.create_Node(NODE_COLUMN_LENGTH))
    if i == 0:
        counter_connections += container.connect_Input_Gate_to_Node_Layer(
            node_layer_list[i])
    elif i == 9:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i-1], node_layer_list[i]
        )
        counter_connections += container.connect_Node_Layer_To_Output_Gate(
            node_layer_list[-1]
        )
    else:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i-1], node_layer_list[i]
        )

print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())
print("Connections:", counter_connections)

for layer in node_layer_list:
    print("Layer Length:", len(layer))

print()
node_layer_list[-1][SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA)
print(
    f"node_layer_list[{SEARCHED_NODE_INDEX}] (id is {node_layer_list[-1][SEARCHED_NODE_INDEX].get_ID()}) contains {node_layer_list[-1][SEARCHED_NODE_INDEX].get_Data()}"
)
print(
    f"Looking for data ({len(node_layer_list)}x{SEARCHED_NODE_INDEX + 1}): {SEARCHED_DATA}"
)

# print("")
# print("===== Sequential Search =====")
# # get the start time
# start_time = time()
# result_queue = container.search(SEARCHED_DATA)
# end_time = time()

# elapsed_time = end_time - start_time
# print('Execution time:', elapsed_time, 'seconds')

# # print("Result Queue:", result_queue)
# print()

# print("Path Length:", len(result_queue))
# for node in result_queue:
#     if node is not None:
#         print(node.get_ID(), end=" > ")
#     else:
#         print("None", end="-")

print("\n")
print("===== Multi-Threaded Search =====")

start_time = time()
found_node_list = container.search_Task([SEARCHED_DATA], True, True)
end_time = time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

print(f"Found {len(found_node_list)} different Node Path")
for node in found_node_list:
    print("ID:", node.get_ID())

_, input_gate, _ = container.get_Struct()
path_checker_result = container.find_Path_By_Checker_Node(
    found_node_list[0],
    input_gate
)
path_checker_result = path_checker_result[:-1]
path_checker_result = path_checker_result[::-1]

print("")
print("Find Path by Checker Result:")
for step in path_checker_result:
    print(step.get_ID(), end=" > ")

print("\n")

# for index, history in enumerate(search_history):
#     # Pass input gate
#     if index == 0:
#         continue
#     print(
#         index,
#         "|",
#         history["parent_node"].get_ID(),
#         history["child_node"].get_ID(),
#         "\t|",
#         history["parent_node_index"],
#         "  \t|",
#         history["result"],
#     )

print("")
