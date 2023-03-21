from time import time
from Classes.Container import Container_Struct
from Classes.Node_PC import COLORS, MARKERS
from Classes.Genetic import Genetic_Environment

NODE_ROW_LENGTH = 50
NODE_COLUMN_LENGTH = 50

# Create a container
container = Container_Struct(
    is_point_cloud=True,
    verbose=True
)

print()
# Create node layers
node_layer_list = list()
counter_connections = 0

# for i, node in enumerate(node_layer_list):
#     node.move(x=2 * i, y=-10, z=0)

node_start = container.create_Node(1, is_point_cloud=True)[0]
node_start.set_Data("Start")
node_start.set_Color(COLORS.RED)
node_start.set_Coordinate(x=0, y=0, z=0)

nodes_row_1 = container.create_Node(5, is_point_cloud=True)
nodes_row_2 = container.create_Node(5, is_point_cloud=True)
nodes_row_3 = container.create_Node(5, is_point_cloud=True)
nodes_row_4 = container.create_Node(5, is_point_cloud=True)

counter_connections += node_start.connect_Node_BiDirection(nodes_row_1[0])

counter_connections += container.connect_Nodes_As_Sequential(
    nodes_row_1, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(
    nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(
    nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_As_Sequential(
    nodes_row_4, bi_direction=True)

counter_connections += container.connect_Nodes_One_O_One(
    nodes_row_1, nodes_row_2, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(
    nodes_row_2, nodes_row_3, bi_direction=True)
counter_connections += container.connect_Nodes_One_O_One(
    nodes_row_3, nodes_row_4, bi_direction=True)

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
counter_connections += node_x_connection.connect_Node_BiDirection(
    nodes_row_4[0])

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
counter_connections += node_y_connection.connect_Node_BiDirection(
    nodes_row_3[0])

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
counter_connections += node_z_connection.connect_Node_BiDirection(
    nodes_row_2[0])

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
counter_connections += node_t_connection.connect_Node_BiDirection(
    nodes_row_1[0])

node_List, input_Gate, output_Gate = container.get_Struct()

counter_connections += input_Gate.connect_Node_BiDirection(node_start)
counter_connections += output_Gate.connect_Node_BiDirection(node_start)
input_Gate.set_Data("input_Gate")
input_Gate.set_Marker(MARKERS.TRIANGLE_UP)
input_Gate.set_Coordinate(x=-10, y=-10, z=0)
output_Gate.set_Data("output_Gate")
output_Gate.set_Marker(MARKERS.TRIANGLE_DOWN)
output_Gate.set_Coordinate(x=-10, y=10, z=0)

# Get gene pool
gene_pool = container.get_Node_List()

# Select Target Node
target = nodes_x[-1]  # gene_pool[-2]
target.set_Color(COLORS.YELLOW)
target.set_Marker(MARKERS.DIAMOND)
target.set_Data("Target Node")

print("Target: ", target.get_ID())
# print("Gene Pool: ", [gene.get_ID() for gene in gene_pool])

print()
print("=== Genetic Algorithm ===")
genetic_env = Genetic_Environment(
    target=target,
    population_number=100,
    gene_pool=gene_pool,
    input_gene=container.get_Input_Gate()
)
# print("Example Chromosome:", genetic_env.create_Chromosome())

# genetic_env.create_Population(unique=True)
# genetic_env.calculate_Fitness_For_Population()
# population = genetic_env.get_Population()
# population_fitnesses = [member.get_Fitness() for member in population]
# print("Fitness Values of Population:", population_fitnesses)

# best_path = [member.get_Chromosome() for member in population if member.get_Fitness() == max(population_fitnesses)]
# print(f"Best Fitness ({max(population_fitnesses)}) Path:", best_path)
start_time = time()
# generation_count = genetic_env.crossover()
best_member, generation_count = genetic_env.autorun(
    minimum_fitness=int(len(gene_pool) * 0.9), 
    unique=True, 
    best_percentage=0.1, 
    evolve_probability=0.5, 
    verbose=True
)
end_time = time()
path = [
    gene.get_ID() for gene in best_member.get_Chromosome()
    if gene is not None
]
path.sort(reverse=True)

print("Generation Count:", generation_count)
print(f"Best Fitness ({best_member.get_Fitness()}) Member:", path)
print("Path Length:", len(path))
print("Process Time:", end_time - start_time)

# path = list()
# for gene in genetic_env.get_Best_Member().get_Chromosome():
#   if gene is not None:
#     path.append(gene.get_ID())
#   else:
#     path.append(None)
# print("Best Path:", path)

print()
print("==== Search Task ===")
start_time = time()
found_node_list = container.search_Task(
    data=["Target Node"], 
    wait_until_k_number_found=1,
    do_not_check_again=True
)
end_time = time()
path_checker_result = container.find_Path_By_Checker_Node(
    found_node_list[0],
    container.get_Input_Gate()
)
path_checker_result = path_checker_result[:-1]
path_checker_result = path_checker_result[::-1]
print("Find Path by Checker Result:")
for step in path_checker_result:
    print(step.get_ID(), end=" > ")
print("")
print("Path Length:", len(path_checker_result))
print("Process Time:", end_time - start_time)

container.plot3D()