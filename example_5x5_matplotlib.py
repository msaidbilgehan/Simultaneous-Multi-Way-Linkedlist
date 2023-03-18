from random import randint, seed
from time import time
from Classes.Container import Container_Struct
import matplotlib.pyplot as plt
import numpy as np

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

seed(time())
SEARCHED_DATA = -13  # randint(0, 100)
NODE_COLUMN_LENGTH = 5  # randint(0, 10000) or cpu_count() * 100
NODE_ROW_LENGTH = 5  # randint(0, 10000) or cpu_count() * 100
SEARCHED_NODE_INDEX = NODE_COLUMN_LENGTH - randint(1, NODE_COLUMN_LENGTH-1)

# Create a container
container = Container_Struct(NUMBER_OF_MAX_WORKERS, is_point_cloud=True)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create NODE_COLUMN_LENGTH x NODE_ROW_LENGTH node layers
node_layer_list = list()
counter_connections = 0
for i in range(NODE_ROW_LENGTH):
    node_layer_list.append(container.create_Node(NODE_COLUMN_LENGTH, True))
    if i == 0:
        counter_connections += container.connect_Input_Gate_to_Node_Layer(
            node_layer_list[i])
        x_tolerance = 10
        for ii, node in enumerate(node_layer_list[i]):
            node.move(x=2 * ii, y=-10, z=0)
    elif i == 9:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i], node_layer_list[i-1]
        )
        counter_connections += container.connect_Node_Layer_To_Output_Gate(
            node_layer_list[-1]
        )
        x_tolerance = 20
        for ii, node in enumerate(node_layer_list[i]):
            node.move(x=5 * ii, y=-10, z=0)
    else:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i], node_layer_list[i-1]
        )
        x_tolerance = 0
        for ii, node in enumerate(node_layer_list[i]):
            node.move(x=7 * ii, y=-10, z=0)

print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())
print("Connections:", counter_connections)

for layer in node_layer_list:
    print("Layer Length:", len(layer))

print()

# https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab
node_list, input_gate, output_Gate = container.get_Struct()

nodes_3D_information = [node.get_Information_3D() for node in node_list]
location_data = [
    node_3D["coordinates"]
    for node_3D in nodes_3D_information
]
location_data_connected = [
    node_3D["connected_coordinates"]
    for node_3D in nodes_3D_information
]

xdata = [ld[0] for ld in location_data]
ydata = [ld[1] for ld in location_data]
zdata = [ld[2] for ld in location_data]

fig = plt.figure(figsize=(9, 6))

# Create 3D container
ax = plt.axes(projection='3d')

# Visualize 3D scatter plot
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='jet')

# Visualize Connections
for i, ld_connected_nodes in enumerate(location_data_connected):
    for ii, ld_connected in enumerate(ld_connected_nodes):
        x_line = np.linspace(xdata[i], ld_connected[0], 2)
        y_line = np.linspace(ydata[i], ld_connected[1], 2)
        z_line = np.linspace(zdata[i], ld_connected[2], 2)
        ax.plot3D(x_line, y_line, z_line, 'blue')

# Give labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Save figure
plt.show()
# plt.savefig('3d_scatter.png', dpi=300)


# node_layer_list[-1][SEARCHED_NODE_INDEX].set_Data(SEARCHED_DATA)
# print(
#     f"node_layer_list[{SEARCHED_NODE_INDEX}] (id is {node_layer_list[-1][SEARCHED_NODE_INDEX].get_ID()}) contains {node_layer_list[-1][SEARCHED_NODE_INDEX].get_Data()}"
# )
# print(
#     f"Looking for data ({len(node_layer_list)}x{SEARCHED_NODE_INDEX + 1}): {SEARCHED_DATA}"
# )

# print("\n")
# print("===== Multi-Threaded Search =====")

# start_time = time()
# found_node_list = container.search_Task([SEARCHED_DATA], True, True)
# end_time = time()
# elapsed_time = end_time - start_time
# print('Execution time:', elapsed_time, 'seconds')

# print(f"Found {len(found_node_list)} different Node Path")
# for node in found_node_list:
#     print("ID:", node.get_ID())

# _, input_gate, _ = container.get_Struct()
# path_checker_result = container.find_Path_By_Checker_Node(
#     found_node_list[0],
#     input_gate
# )
# path_checker_result = path_checker_result[:-1]
# path_checker_result = path_checker_result[::-1]
# print("")
# print("Find Path by Checker Result:")
# for step in path_checker_result:
#     print(step.get_ID(), end=" > ")

# print("")
