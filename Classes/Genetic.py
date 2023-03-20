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
      self.population = list()
      self.next_generation = list()
      self.generation_count = 0
      self.population_history = list()
      
    def random_Gene(self):
      return random.choice(self.gene_pool)
      
    def random_Gene_From_Parent(self, parent_gene):
      connected_genes = parent_gene.get_Connected_Node_List()
      if len(connected_genes) > 0:
        return random.choice(connected_genes)
      else:
        return None
    
    @staticmethod
    def latest_Gene(chromosome):
      for i in range(len(chromosome) - 1, -1, -1):
        if chromosome[i] is not None:
            return chromosome[i]
      return None
    
    def create_Chromosome(self, unique:bool) -> list:
      if unique:
        chromosome = list()
        for _ in range(len(self.gene_pool)):
          if len(chromosome) == 0:
            gene = self.random_Gene_From_Parent(self.input_gene)
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
      
    def get_Population(self) -> list:
      return self.population
      
    def calculate_Fitness(self, member):
      fitness = 0
      for gene in member.get_Chromosome():
        if gene == self.target:
          fitness += 10
          break
        else:
          fitness -= 1
      member.fitness = fitness
      
    def calculate_Fitness_For_Population(self):
      for member in self.population:
        self.calculate_Fitness(member)
        
    def get_Best_Member(self):
      return max(self.population, key=lambda member: member.get_Fitness())
    
    def sort_Population(self):
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
            child.append(parent1[i])
          else:
            child.append(parent2[i])
        else:
          # Crossover
          for i in range(len(parent1)):
            if i % 2 == 0:
              child.append(parent1[i])
            else:
              child.append(parent2[i])
      return child
      
    def autorun(self):
      self.create_Population(unique=True)
      self.calculate_Fitness_For_Population()
      generation_count = 0
      while self.get_Best_Member_Fitness() < 10:
        generation_count += self.crossover(
            unique=True, best_percentage=0.1, evolve_probability=0.1)
        self.calculate_Fitness_For_Population()
      return self.get_Best_Member(), generation_count
      
class Member():
  def __init__(self, chromosome):
    self.chromosome = chromosome
    self.fitness = 0
  
  def get_Chromosome(self) -> list:
    return self.chromosome
  
  def get_Fitness(self) -> int:
    return self.fitness