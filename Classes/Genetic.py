import random
from Classes.Node import Node_Struct
from Classes.Node_PC import Node_Point_Cloud_Struct
from Classes.Gate import Gate_Struct, Gate_Point_Cloud_Struct

class Genetic_Environment():
    def __init__(
      self, 
      target: Node_Struct or Node_Point_Cloud_Struct, 
      population_number: int, 
      gene_pool: list, 
      input_gene: Node_Struct or Node_Point_Cloud_Struct or Gate_Struct or Gate_Point_Cloud_Struct
    ):
      
      self.target = target
      self.input_gene = input_gene
      self.gene_pool = gene_pool
      self.population_number = population_number
      self.population = list()
      self.next_generation = list()
      self.generation_count = 0
      self.population_history = list()
      
    def reset_Genetic(self):
      """
      Resets the genetic algorithm.
      """
      self.population = list()
      self.next_generation = list()
      self.generation_count = 0
      self.population_history = list()
      
    def random_Gene(self):
      """
      Returns a random gene from the gene pool.
      """
      return random.choice(self.gene_pool)
      
    def random_Gene_From_Parent(self, parent_gene):
      """
      Returns a random gene from the parent gene's connected node list.
      """
      connected_genes = parent_gene.get_Connected_Node_List()
      if len(connected_genes) > 0:
        return random.choice(connected_genes)
      return None
    
    @staticmethod
    def latest_Gene(chromosome):
      """
      Returns the latest gene in a chromosome.
      """
      # Iterate over the chromosome backwards
      for i in range(len(chromosome) - 1, -1, -1):
          # If a gene is found, return it
          if chromosome[i] is not None:
              return chromosome[i]
      # If no gene is found, return None
      return None
    
    def create_Chromosome(self, unique:bool) -> list:
      if unique:
        chromosome = list()
        for _ in range(len(self.gene_pool)):
          if len(chromosome) == 0:
            gene = self.input_gene
          else:
            if None in chromosome:
              latest_gene = self.latest_Gene(chromosome)
            else:
              latest_gene = chromosome[-1]
            gene = self.random_Gene_From_Parent(latest_gene)
          if gene not in chromosome:
            chromosome.append(gene)
          else:
            chromosome.append(None)
        return chromosome
      else:
        return [
            self.random_Gene()
            for _ in range(len(self.gene_pool))
        ]
      
    def create_Population(self, unique:bool):
      self.population = [
          Member(self.create_Chromosome(unique))
          for _ in range(self.population_number)
        ]
      
      # TODO: Remove this! Sometimes chromosome length is less than gene pool length
      for member in self.population:
        if len(member.get_Chromosome()) < len(self.gene_pool):
          raise ValueError(f"Chromosome length is less than gene pool length ({len(member.get_Chromosome())} < {len(self.gene_pool)})")
      
    def get_Population(self) -> list:
      return self.population
      
    def calculate_Fitness(self, member):
      fitness = 0
      for i, gene in enumerate(member.get_Chromosome()):
        # fitness += 10 if gene == self.target else -1
        if gene == self.target:
          fitness += (len(self.gene_pool) - i)
          break
        else:
          fitness -= 1
      member.fitness = fitness
    
    def calculate_Fitness_For_Population(self):
        # Calculate the fitness for each member in the population
        for member in self.population:
            self.calculate_Fitness(member)

    def get_Best_Member(self):
        # Return the member with the highest fitness
        return max(self.population, key=lambda member: member.get_Fitness())
    
    def sort_Population(self):
      # Sort the population by fitness (descending order)
      self.population.sort(key=lambda member: member.get_Fitness(), reverse=True)
    
    def get_Best_Member_Fitness(self) -> int:
      return self.get_Best_Member().get_Fitness()
    
    def get_Best_Member_Chromosome(self):
      return self.get_Best_Member().get_Chromosome()
    
    def crossover(self, unique: bool = True, best_percentage=0.1, evolve_probability=0.1) -> int:
      self.sort_Population()

      self.next_generation = list()
      
      # Add the best members to the next generation
      best_members = self.population[
        :int(self.population_number * best_percentage)
      ]
      self.next_generation.extend(best_members)
      
      # Add the rest of the members to the next generation
      while self.next_generation.__len__() < self.population_number:
        parent1 = random.choice(best_members)
        parent2 = random.choice(best_members)
        while len(parent1.get_Chromosome()) != len(parent2.get_Chromosome()):
          parent1 = random.choice(best_members)
          parent2 = random.choice(best_members)
        
        # Crossover
        child = self.__crossover(
          parent1.get_Chromosome(), 
          parent2.get_Chromosome(), 
          unique=unique,
          evolve=True, 
          evolve_probability=evolve_probability
        )
        self.next_generation.append(Member(child))
        self.generation_count += 1
        
      self.population_history.append(self.population)
      self.population = self.next_generation
      return self.generation_count
      
    def __crossover(self, parent1, parent2, unique:bool, evolve:bool, evolve_probability:float):
      if len(parent1) != len(parent2):
        raise ValueError("Parents have different chromosome lengths.")
      
      child = list()
      
      # Evolve or Crossover
      for i in range(len(parent1)):
        # Evolve
        if evolve:
          # Evolve Probability
          e_probability = random.random()
          if e_probability < evolve_probability:
            # Evolve Gene
            while unique:
              gene = self.random_Gene()
              if gene not in child:
                child.append(gene)
                break
            else:
              child.append(self.random_Gene())
          elif e_probability < evolve_probability * 2:
            count_repeat = 0
            while unique and count_repeat < 3:
              if parent1[i] is None:
                child.append(None)
                break
              elif parent1[i] not in child:
                child.append(None)
                break
              else:
                gene = self.random_Gene_From_Parent(parent1[i])
                if gene is None:
                  child.append(gene)
                  break
                elif gene not in child:
                  child.append(gene)
                  break
                else:
                  count_repeat += 1
            if not unique:
              child.append(parent1[i])
          else:
            count_repeat = 0
            while unique and count_repeat < 3:
              if parent2[i] is None:
                child.append(None)
                break
              elif parent2[i] not in child:
                child.append(None)
                break
              else:
                gene = self.random_Gene_From_Parent(parent2[i])
                if gene is None:
                  child.append(gene)
                  break
                elif gene not in child:
                  child.append(gene)
                  break
                else:
                  count_repeat += 1
            if not unique:
              child.append(parent2[i])
        else:
          # Crossover
          for i in range(len(parent1)):
            if i % 2 == 0:
              child.append(parent1[i])
            else:
              child.append(parent2[i])
      return child
      
    def autorun(self, minimum_fitness: int = 10, unique: bool = True, best_percentage: float = 0.1, evolve_probability: float = 0.1, verbose: bool = False):
      if verbose:
        print(f"Parameters:\n\t-> Minimum Fitness: {minimum_fitness}\n\t-> Unique: {unique}\n\t-> Best Percentage: {best_percentage}\n\t-> Evolve Probability: {evolve_probability}\n\t-> Verbose: {verbose}")
      self.create_Population(unique=True)
      if verbose:
        print("Population Created.")
      self.calculate_Fitness_For_Population()
      if verbose:
        print("Fitness Calculated.")
      i = 0
      while self.get_Best_Member_Fitness() < minimum_fitness:
        self.crossover(
            unique=unique,
            best_percentage=best_percentage, 
            evolve_probability=evolve_probability
        )
        self.calculate_Fitness_For_Population()
        if verbose:
          print(f"{i}. Crossover Best Fitness is {self.get_Best_Member_Fitness()}", end="\r")
        i += 1
      if verbose:
        print()
      return self.get_Best_Member(), self.generation_count
      
class Member():
  def __init__(self, chromosome):
    self.chromosome = chromosome
    self.fitness = 0
  
  def get_Chromosome(self) -> list:
    return self.chromosome
  
  def get_Fitness(self) -> int:
    return self.fitness