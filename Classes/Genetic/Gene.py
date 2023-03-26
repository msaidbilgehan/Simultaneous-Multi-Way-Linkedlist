import random
from typing import Self
from typing import Union
from Classes.Node import Node_Struct
from Classes.Node_PC import Node_Point_Cloud_Struct
from Classes.Gate import Gate_Struct, Gate_Point_Cloud_Struct

class Gene():
  def __init__(self, gene: Union[Node_Struct, Node_Point_Cloud_Struct, Gate_Struct, Gate_Point_Cloud_Struct]):
    self.gene = gene
    
  def get_Gene(self):
    return self.gene
  
  def get_Connected_Genes(self) -> list[Self]:
    connected_nodes = self.gene.get_Connected_Node_List()
    connected_genes = list()
    for node in connected_nodes:
      connected_genes.append(Gene(node))
    return connected_genes
  
  def is_Connected(self, gene:Self):
    return gene.gene in self.gene.get_Connected_Node_List()
  
  def get_Connected_Gene(self, index: int) -> Union[Node_Struct, Node_Point_Cloud_Struct, Gate_Struct, Gate_Point_Cloud_Struct]:
    return self.gene.get_Connected_Node_List()[index]
  
  def get_Connected_Gene_Count(self) -> int:
    return len(self.gene.get_Connected_Node_List())
  
  def get_Random_Connected_Gene(self) -> Self:
    if len(self.gene.get_Connected_Node_List()) == 0:
      return self
    return Gene(random.choice(self.gene.get_Connected_Node_List()))
  
  def evolve(self) -> Self:
    return self.get_Random_Connected_Gene()
