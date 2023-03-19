from random import randint, seed
from time import time
from Classes.Container import Container_Struct

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

seed(time())
SEARCHED_DATA = -13  # randint(0, 100)
NODE_COLUMN_LENGTH = 3  # randint(0, 10000) or cpu_count() * 100
NODE_ROW_LENGTH = 3  # randint(0, 10000) or cpu_count() * 100
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
            node.set_Coordinate(x=ii, y=i, z=0)
    elif i == 4:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i], node_layer_list[i-1]
        )
        counter_connections += container.connect_Node_Layer_To_Output_Gate(
            node_layer_list[-1]
        )
        x_tolerance = 20
        for ii, node in enumerate(node_layer_list[i]):
            node.set_Coordinate(x=ii, y=4, z=1)
    else:
        counter_connections += container.connect_Node_Layers(
            node_layer_list[i], node_layer_list[i-1]
        )
        x_tolerance = 0
        for ii, node in enumerate(node_layer_list[i]):
            node.set_Coordinate(x=ii, y=i, z=0.5)

print()
print("=== Node Layers ===")
print("Node Number:", container.get_Node_Number())
print("Blocked Node Number:", container.get_Blocked_Node_Number())
print("Connections:", counter_connections)

for layer in node_layer_list:
    print("Layer Length:", len(layer))

print()

# https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab
# https://matplotlib.org/stable/gallery/animation/random_walk.html

node_list, input_gate, output_Gate = container.get_Struct()
input_gate.set_Coordinate(x=-2, y=0, z=-1)
output_Gate.set_Coordinate(x=10 , y=7, z=1)

nodes_ID_information = [node.get_ID() for node in node_list]
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

#########################################
#########################################
#########################################

# Fixing random state for reproducibility


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


# Data: walks as arrays
walks = list()
num_steps = 100

for i, ld in enumerate(location_data):
    for ldc in location_data_connected[i]:
        walks.append(
            walk(
                start_pos=ld,
                end_pos=ldc,
                num_steps=num_steps
            )
        )

# Attaching 3D axis to the figure
# fig = plt.figure(figsize=(9, 6))
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(projection="3d")

# Create lines initially without data
lines = [ax.plot([], [], [])[0] for _ in walks]

# Setting the axes properties
ax.set(xlim3d=(0, 1), xlabel='X')
ax.set(ylim3d=(0, 1), ylabel='Y')
ax.set(zlim3d=(0, 1), zlabel='Z')

# Creating the Animation object
anim = animation.FuncAnimation(
    fig, 
    update_lines, 
    num_steps, 
    fargs=(walks, lines), 
    interval=100,
    repeat=False
)

# Visualize 3D scatter plot
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='jet', s=70)
ax.view_init(elev=25, azim=-30)
ax.autoscale(enable=True, axis='both', tight=None)

for i, id in enumerate(nodes_ID_information):
    ax.text(xdata[i], ydata[i], zdata[i], id, color='red')

# # Visualize Connections
# for i, ld_connected_nodes in enumerate(location_data_connected):
#     for ii, ld_connected in enumerate(ld_connected_nodes):
#         x_line = np.linspace(xdata[i], ld_connected[0], 2)
#         y_line = np.linspace(ydata[i], ld_connected[1], 2)
#         z_line = np.linspace(zdata[i], ld_connected[2], 2)
#         ax.plot3D(x_line, y_line, z_line, 'blue')

# # Give labels
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# Show figure
plt.show()

writer_gif = animation.PillowWriter(fps=30)
anim.save(r"animation.gif", writer=writer_gif)

# f = r"animation.mp4"
# writer_video = animation.FFMpegWriter(fps=60)
# anim.save(f, writer=writer_video)
