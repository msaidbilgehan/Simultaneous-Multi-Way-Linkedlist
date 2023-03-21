from time import time
from Classes.Container import Container_Struct

print("")
print("=== Initialize ===")
NUMBER_OF_MAX_WORKERS = 10000

# Create a container
container = Container_Struct(
    NUMBER_OF_MAX_WORKERS, 
    is_point_cloud=True, 
    verbose=False
)
# container.set_Max_Workers(NUMBER_OF_MAX_WORKERS)

print("Max Workers:", container.get_Max_Workers())

# Create node layers
node_layer_list = list()
counter_connections = 0

# for i, node in enumerate(node_layer_list):
#     node.move(x=2 * i, y=-10, z=0)

node_start = container.create_Node(1, is_point_cloud=True)[0]
node_start.set_Data("Start")
node_start.set_Coordinate(x=0, y=0, z=0)

nodes_row_1 = container.create_Node(5, is_point_cloud=True)
nodes_row_2 = container.create_Node(5, is_point_cloud=True)
nodes_row_3 = container.create_Node(5, is_point_cloud=True)
nodes_row_4 = container.create_Node(5, is_point_cloud=True)

counter_connections += node_start.connect_Node_BiDirection(nodes_row_1[0])

counter_connections += container.connect_Nodes_As_Sequential(nodes_row_1, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(nodes_row_4, bi_direction=True)

counter_connections += container.connect_Nodes_One_O_One(nodes_row_1, nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(nodes_row_2, nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(nodes_row_3, nodes_row_4, bi_direction=True)

for i, node in enumerate(nodes_row_1):
    node.set_Data(f"nodes_row_1:{i}")
    node.set_Coordinate(x=10, y=i * 10, z=0)

for i, node in enumerate(nodes_row_2):
    node.set_Data(f"nodes_row_2:{i}")
    node.set_Coordinate(x=20, y=i * 10, z=0)

for i, node in enumerate(nodes_row_3):
    node.set_Data(f"nodes_row_3:{i}")
    node.set_Coordinate(x=30, y=i * 10, z=0)

for i, node in enumerate(nodes_row_4):
    node.set_Data(f"nodes_row_4:{i}")
    node.set_Coordinate(x=40, y=i * 10, z=0)

nodes_x = container.create_Node(3, is_point_cloud=True)
node_x_connection = container.create_Node(1, is_point_cloud=True)[0]
node_x_connection.set_Data(f"node_x_connection")
counter_connections += container.connect_Nodes_To_Node(
    nodes_x, 
    node_x_connection, 
    bi_direction=True
)
node_x_connection.set_Coordinate(x=40, y=-15, z=0)
for i, node in enumerate(nodes_x):
    node.set_Data(f"nodes_x:{i}")
    node.set_Coordinate(x=35 + (i*4), y=-25, z=0)

# for node in nodes_x:
#     counter_connections += node.connect_Node_BiDirection(node_x_connection)
counter_connections += node_x_connection.connect_Node_BiDirection(nodes_row_4[0])

nodes_y = container.create_Node(3, is_point_cloud=True)
node_y_connection = container.create_Node(1, is_point_cloud=True)[0]
node_y_connection.set_Data(f"node_y_connection")
counter_connections += container.connect_Nodes_To_Node(
    nodes_y,
    node_y_connection,
    bi_direction=True
)
node_y_connection.set_Coordinate(x=30, y=-15, z=0)
for i, node in enumerate(nodes_y):
    node.set_Data(f"nodes_y:{i}")
    node.set_Coordinate(x=25 + (i*4), y=-25, z=0)

# for node in nodes_y:
#     counter_connections += node.connect_Node_BiDirection(node_y_connection)
counter_connections += node_y_connection.connect_Node_BiDirection(nodes_row_3[0])

nodes_z = container.create_Node(3, is_point_cloud=True)
node_z_connection = container.create_Node(1, is_point_cloud=True)[0]
node_z_connection.set_Data(f"node_z_connection")
counter_connections += container.connect_Nodes_To_Node(
    nodes_z,
    node_z_connection,
    bi_direction=True
)
node_z_connection.set_Coordinate(x=20, y=-15, z=0)
for i, node in enumerate(nodes_z):
    node.set_Data(f"nodes_z:{i}")
    node.set_Coordinate(x=15 + (i*4), y=-25, z=0)

# for node in nodes_z:
#     counter_connections += node.connect_Node_BiDirection(node_z_connection)
counter_connections += node_z_connection.connect_Node_BiDirection(nodes_row_2[0])

nodes_t = container.create_Node(3, is_point_cloud=True)
node_t_connection = container.create_Node(1, is_point_cloud=True)[0]
node_t_connection.set_Data(f"node_t_connection")
counter_connections += container.connect_Nodes_To_Node(
    nodes_t,
    node_t_connection,
    bi_direction=True
)
node_t_connection.set_Coordinate(x=10, y=-15, z=0)
for i, node in enumerate(nodes_t):
    node.set_Data(f"nodes_t:{i}")
    node.set_Coordinate(x=5 + (i*4), y=-25, z=0)

# for node in nodes_t:
#     counter_connections += node.connect_Node_BiDirection(node_t_connection)
counter_connections += node_t_connection.connect_Node_BiDirection(nodes_row_1[0])

node_List, input_Gate, output_Gate = container.get_Struct()

counter_connections += input_Gate.connect_Node_BiDirection(node_start)
counter_connections += output_Gate.connect_Node_BiDirection(node_start)
input_Gate.set_Data("input_Gate")
input_Gate.set_Coordinate(x=-10, y=-10, z=0)
output_Gate.set_Data("output_Gate")
output_Gate.set_Coordinate(x=-10, y=10, z=0)

container.plot3D()