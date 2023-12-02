from typing import Union
from Classes.Genetic.Gene import Gene
import secrets

class Chromosome():
  def __init__(self, genes: list[Gene]):
    self.genes = genes
    
  def get_Genes(self) -> list[Gene]:
    return self.genes
  
  def get_Gene(self, index:int):
    return self.genes[index]
  
  def get_Gene_Count(self):
    return len(self.genes)
  
  def get_Random_Gene(self):
    return secrets.SystemRandom().choice(self.genes)
  
  def get_Latest_Gene(self):
    # Iterate over the chromosome backwards
    for i in range(len(self.genes) - 1, -1, -1):
        # If a gene is found, return it
        if self.genes[i] is not None:
            return self.genes[i]
    # If no gene is found, return None
    return None
  
  def get_Distance(self, target: Gene):
    """
    Returns the distance between the latest gene and the target.
    """
    # Calculate the distance
    distance = 0
    target_gene_found = False
    for i in range(len(self.genes) - 1):
      if target == self.genes[i]:
        target_gene_found = True
        break
      elif self.genes[i] is None:
        distance += 1
        break
      else:
        distance += 1
        
    # Return the distance
    return distance, target_gene_found

  def get_Distance_Reward(self, target: Gene):
    """
    Returns the distance reward between the latest gene and the target.
    """
    # Calculate the reward
    reward = 0
    target_gene_found = False
    for i in range(len(self.genes) - 1):
      if target == self.genes[i]:
        target_gene_found = True
        reward += 100
        break
      elif self.genes[i] is None:
        reward -= 10
      else:
        reward -= 1
      
    # Return the reward
    return reward, target_gene_found
  
  def evolve(self):
    genes = self.get_Genes()
    selected_gene = self.get_Random_Gene()
    
    if selected_gene is None:
      return
    
    selected_gene_index = genes.index(selected_gene)
    evolved_gene = selected_gene.evolve()

    genes[selected_gene_index] = evolved_gene
    for i in range(selected_gene_index, len(genes)):
      if i == selected_gene_index:
        genes[i] = None
        
    self.genes = genes
    
  def fitness_reward(self, target: Gene):
    """
    Returns the fitness of the chromosome.
    """
    # Calculate the fitness
    fitness, target_gene_found = self.get_Distance_Reward(target)
    
    # Return the fitness
    return fitness, target_gene_found
    
  def fitness_distance(self, target: Gene):
    """
    Returns the fitness of the chromosome.
    """
    # Calculate the fitness
    distance, target_gene_found = self.get_Distance(target)
    if target_gene_found:
        fitness = 1
    else:
      if distance == 0:
        fitness = 0
      else:
        fitness = 1 / distance
    # Return the fitness
    return fitness, target_gene_found
    
