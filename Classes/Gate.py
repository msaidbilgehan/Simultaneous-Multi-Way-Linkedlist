
from Classes.Node import Node_Struct


class Gate_Struct(Node_Struct):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_List = list()
        self.input_List = list()
        
    def task(self, args):
        self.output_List = self.input_Calculator(self.input_List)

    def input_Calculator(self, input):
        # Override this method
        # Do Something
        pass

    def get_Output(self):
        return self.output_List
    
    def add_Input(self, input):
        self.input_List.append(input)
        
