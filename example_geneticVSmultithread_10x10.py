from time import time
from Classes.Container import Container_Struct
from Classes.Genetic import Genetic_Environment

NODE_ROW_LENGTH = 50
NODE_COLUMN_LENGTH = 50

# Create a container
container = Container_Struct(verbose=True)

print()
print("=== Create Nodes ===")

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

# Get gene pool
gene_pool = container.get_Node_List()

# Select Target Node
target = gene_pool[-2]
target.set_Data("Target Node")

print("Target: ", target.get_ID())
# print("Gene Pool: ", [gene.get_ID() for gene in gene_pool])

print()
print("=== Genetic Algorithm ===")
genetic_env = Genetic_Environment(
    target=target,
    population_number=500,
    gene_pool=gene_pool,
    input_gene=container.get_Input_Gate()
)
# print("Example Chromosome:", genetic_env.create_Chromosome())

genetic_env.create_Population(unique=True)
genetic_env.calculate_Fitness_For_Population()
# population = genetic_env.get_Population()
# population_fitnesses = [member.get_Fitness() for member in population]
# print("Fitness Values of Population:", population_fitnesses)

# best_path = [member.get_Chromosome() for member in population if member.get_Fitness() == max(population_fitnesses)]
# print(f"Best Fitness ({max(population_fitnesses)}) Path:", best_path)
start_time = time()
# generation_count = genetic_env.crossover()
best_member, generation_count = genetic_env.autorun(
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
found_node_list = container.search_Task(["Target Node"], 1)
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
