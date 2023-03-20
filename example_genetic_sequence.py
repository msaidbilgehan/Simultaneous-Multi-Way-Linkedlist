from Classes.Container import Container_Struct
from Classes.Genetic import Genetic_Environment

# Create a container
container = Container_Struct()

# Create a gene pool
gene_pool = container.create_Node(10)

# Connect the first node to the input gate
container.connect_Node_As_Ordered()

# Select Target Node
target = gene_pool[-5]

print("Target: ", target.get_ID())
print("Gene Pool: ", [gene.get_ID() for gene in gene_pool])

genetic_env = Genetic_Environment(
    target=target,
    population_number=1000,
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
generation_count = genetic_env.crossover()

print("Generation Count:", generation_count)
print(f"Best Fitness ({genetic_env.get_Best_Member_Fitness()}) Member:",
      [gene.get_ID() for gene in genetic_env.get_Best_Member().get_Chromosome()]
    )
