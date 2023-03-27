from copy import copy
import random
import time
from typing import Union
from Classes import Node
from Classes.Node import Node_Struct
from Classes.Node_PC import Node_Point_Cloud_Struct
from Classes.Gate import Gate_Struct, Gate_Point_Cloud_Struct
from Classes.Genetic.Gene import Gene
from Classes.Genetic.Chromosome import Chromosome

class Genetic_Environment():
    def __init__(
      self, 
      chromosome_length_limit: int,
      population_number: int, 
    ):
      self.input_gene = None
      self.gene_pool = list()

      self.chromosome_length_limit = chromosome_length_limit
      self.population_number = population_number
      self.population = list()
      self.next_generation = list()
      self.generation_count = 0
      self.population_history = list()
      
    def initialize_environment(
      self,
      input_gene: Union[Gene, Node_Struct, Node_Point_Cloud_Struct, Gate_Struct, Gate_Point_Cloud_Struct],
      gene_pool: list[Union[Gene, Node_Struct, Node_Point_Cloud_Struct, Gate_Struct, Gate_Point_Cloud_Struct]],
    ) -> None:
      """
      Initializes the genetic algorithm.
      """
      if type(input_gene) is not Gene:
        self.input_gene = Gene(input_gene)  # type: ignore
      else:
        self.input_gene = input_gene

      self.gene_pool = list()
      for gene in gene_pool:
        if type(gene) is not Gene:
          self.gene_pool.append(Gene(gene))  # type: ignore
        else:
          self.gene_pool.append(gene)
      self.reset_Genetic()
      self.create_Population()
      
    def reset_Genetic(self) -> None:
      """
      Resets the genetic algorithm.
      """
      self.population = list()
      self.next_generation = list()
      self.generation_count = 0
      self.population_history = list()
      
    def convert_Nodes_To_Genes(self, nodes: list[Union[Node_Struct, Node_Point_Cloud_Struct, Gate_Struct, Gate_Point_Cloud_Struct]]) -> list[Gene]:
      """
      Converts a list of nodes to a list of genes.
      """
      genes = list()
      for node in nodes:
        genes.append(Gene(node))
      return genes
      
    def set_Gene_Pool(self, gene_pool: list[Gene]) -> None:
      """
      Sets the gene pool.
      """
      self.gene_pool = gene_pool
      
    def get_Gene_Pool(self) -> list[Gene]:
      """
      Returns the gene pool.
      """
      return self.gene_pool
    
    def get_Population(self) -> list[Chromosome]:
      """
      Returns the population.
      """
      return self.population
    
    def create_Population(self) -> None:
      """
      Creates the initial population.
      """
      if self.input_gene is None:
        raise Exception("Input gene is None. First set the input gene!")

      for _ in range(self.population_number):
        genes = list()
        genes.append(self.input_gene)
        genes.extend([
            None for _ in range(1, self.chromosome_length_limit)
        ])
        self.population.append(Chromosome(genes))
    
    def get_best_fitness_chromosome(self, target:Gene) -> tuple:
      best_fitness = -10
      best_chromosome = None
      is_found = False
      for chromosome in self.get_Population():
        fitness, found = chromosome.fitness_reward(target)
        if fitness > best_fitness:
          best_fitness = fitness
          best_chromosome = chromosome
          is_found = found
      
      return best_chromosome, best_fitness, is_found

    def get_population_total_fitness(self, target:Gene) -> float:
      total_fitness = 0
      for chromosome in self.get_Population():
        fitness, _ = chromosome.fitness_reward(target)
        total_fitness += fitness
      
      return total_fitness / len(self.get_Population())

    def get_population_fitness(self, target:Gene) -> list[tuple[float, bool]]:
      population_fitness = list()
      for chromosome in self.get_Population():
        population_fitness.append(chromosome.fitness_reward(target))
      return population_fitness

    def sort_population(self, target:Gene):
      # Sort the population by fitness (descending order)
      self.population.sort(
          key=lambda chromosome: chromosome.fitness_reward(target)[0],
        reverse=True
      )
      
    def step_next_generation(self, target:Gene, best_percentage=0.1, evolve_probability=0.1) -> int:
      self.sort_population(target)

      self.next_generation = list()

      # Add the best members to the next generation
      best_members = self.population[
          :int(self.population_number * best_percentage)
      ]
      self.next_generation.extend(best_members)
      
      # Add the rest of the members to the next generation
      while len(self.next_generation) < self.population_number:
        parent_chromosome_1 = random.choice(best_members)
        parent_chromosome_2 = random.choice(best_members)

        # if parent_chromosome_1.genes is [None] or parent_chromosome_2.genes is [None]:
        #   raise Exception("Parent chromosome is None!")

        random.seed(time.time())
        step_evolve_probability = random.random()
        if step_evolve_probability < evolve_probability:
            random.seed(time.time())
            parent_chromosome_evolved = copy(
              parent_chromosome_1 if random.randint(0, 1) else
              parent_chromosome_2
            )
            self.next_generation.append(parent_chromosome_evolved)
        else:
            # crossover_chromosome = self.crossover(
            #     parent_chromosome_1,
            #     parent_chromosome_2
            # )
            # self.next_generation.append(crossover_chromosome)
            # self.generation_count += 1
            evolved_chromosome_1, evolved_chromosome_2 = self.evolve(
                parent_chromosome_1,
                parent_chromosome_2
            )
            self.next_generation.append(evolved_chromosome_1)
            self.next_generation.append(evolved_chromosome_2)
            self.generation_count += 2

      self.population_history.append(self.population)
      self.population = self.next_generation.copy()
      return self.generation_count

    def crossover(self, parent_chromosome_1, parent_chromosome_2):
      child_genes = list()
      for i in range(self.chromosome_length_limit):
        random.seed(time.time())
        if i == 0:
          child_genes.append(parent_chromosome_1.get_Gene(i))
          continue
        else:
          if random.randint(0, 1):
            crossover_gene = parent_chromosome_1.get_Gene(i)
          else:
            crossover_gene = parent_chromosome_2.get_Gene(i)
          
          if crossover_gene is not None:
            if child_genes[i - 1].is_Connected(crossover_gene):
              child_genes.append(crossover_gene)
            else:
              child_genes.append(child_genes[i - 1].evolve())
          else:
            child_genes.append(child_genes[i - 1].evolve())

      return Chromosome(child_genes)
    
    def evolve(self, parent_chromosome_1, parent_chromosome_2) -> tuple[Chromosome, Chromosome]:
      parent_1_child_genes = list()
      parent_2_child_genes = list()
      parent_1_child_genes.append(parent_chromosome_1.get_Gene(0))
      parent_2_child_genes.append(parent_chromosome_2.get_Gene(0))
      for _ in range(1, self.chromosome_length_limit):
        parent_1_child_genes.append(parent_1_child_genes[-1].evolve())
        parent_2_child_genes.append(parent_2_child_genes[-1].evolve())
        
      return Chromosome(parent_1_child_genes), Chromosome(parent_2_child_genes)

    def autorun(self, target: Gene, max_generations: int = 1000, best_percentage=0.1, evolve_probability=0.1):
      while max_generations:
        self.step_next_generation(
          target,
          best_percentage=best_percentage,
          evolve_probability=evolve_probability
        )
        # self.sort_population()
        best_chromosome, best_fitness, is_found = self.get_best_fitness_chromosome(target)
        print(
            f"{self.generation_count}. Generation Best Fitness {best_fitness}",
          end="\r"
        )
        max_generations -= 1
      print()
      return self.get_best_fitness_chromosome(target)
        
        
        