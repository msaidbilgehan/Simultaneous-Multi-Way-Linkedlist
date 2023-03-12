from random import randint, seed
from time import time
from Classes.Container import Container_Struct

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

seed(time())
SEARCHED_DATA = -13  # randint(0, 100)
NODE_COLUMN_LENGTH = 4  # randint(0, 10000) or cpu_count() * 100
NODE_ROW_LENGTH = 4  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_COLUMN_LENGTH - randint(1, NODE_COLUMN_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_COLUMN_LENGTH x NODE_ROW_LENGTH node layers
node_layer_list = list()
counter_connections = 0

nodes_row_1 = container.create_Node(5)
nodes_row_2 = container.create_Node(5)
nodes_row_3 = container.create_Node(5)
nodes_row_4 = container.create_Node(5)

node_start = container.create_Node(1)[0]
counter_connections += node_start.connect_Two_Way_Node(nodes_row_4[-1])

counter_connections += container.connect_Nodes_As_Sequential(nodes_row_1, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_4, bi_direction=True)

counter_connections += container.connect_Nodes_One_O_One(nodes_row_1, nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(nodes_row_2, nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(nodes_row_3, nodes_row_4, bi_direction=True)

nodes_x = container.create_Node(3)
node_x_connection = container.create_Node(1)[0]
for node in nodes_x:
    counter_connections += node.connect_Two_Way_Node(node_x_connection)
counter_connections += node_x_connection.connect_Two_Way_Node(nodes_row_1[-1])

nodes_y = container.create_Node(3)
node_y_connection = container.create_Node(1)[0]
for node in nodes_y:
    counter_connections += node.connect_Two_Way_Node(node_y_connection)
counter_connections += node_y_connection.connect_Two_Way_Node(nodes_row_2[-1])

nodes_z = container.create_Node(3)
node_z_connection = container.create_Node(1)[0]
for node in nodes_z:
    counter_connections += node.connect_Two_Way_Node(node_z_connection)
counter_connections += node_z_connection.connect_Two_Way_Node(nodes_row_3[-1])

nodes_t = container.create_Node(3)
node_t_connection = container.create_Node(1)[0]
for node in nodes_t:
    counter_connections += node.connect_Two_Way_Node(node_t_connection)
counter_connections += node_t_connection.connect_Two_Way_Node(nodes_row_4[-1])

node_List, input_Gate, output_Gate = container.get_Struct()

counter_connections += node_start.connect_Two_Way_Node(input_Gate)


print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())
print("Connections:", counter_connections)

print()
nodes_row_1[0].set_Data(SEARCHED_DATA)
print(
    f"nodes_row_1[0] (id is {nodes_row_1[0].id}) contains {nodes_row_1[0].get_Data()}"
)
print(
    f"Looking for data: {SEARCHED_DATA}"
)

print("")
print("===== Sequential Search =====")
# get the start time
start_time = time()
result_queue = container.search(SEARCHED_DATA)
end_time = time()

elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')


for node in result_queue:
    if node is not None:
        print(node.id, end=" > ")
    else:
        print("None", end="-")
print()
print("Path Length:", len(result_queue))

print("\n")
print("===== Multi-Threaded Search =====")

start_time = time()
found_node_list = container.search_Task(SEARCHED_DATA, True, True)
end_time = time()
elapsed_time = end_time - start_time
print('Execution time:', elapsed_time, 'seconds')

print(f"Found {len(found_node_list)} different Node Path")
# for node in found_node_list:
#     print("ID:", node.id)

path_checker_result = container.find_Path_By_Checker_Node(
    found_node_list[0],
    input_Gate
)
path_checker_result = path_checker_result[:-1]
path_checker_result = path_checker_result[::-1]
print("")
print("Find Path by Checker Result:")
for step in path_checker_result:
    print(step.id, end=" > ")
    
print()
print("Path Length:", len(path_checker_result))
print()

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

print("")
