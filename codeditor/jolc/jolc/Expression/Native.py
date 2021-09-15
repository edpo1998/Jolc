from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Error import *
from codeditor.jolc.jolc.Expression.EnvNative import FuncNative as Nativa


class Native(Tree):
    def __init__(self,typefunction=None,parameters=None,row = None, col =None):
        super().__init__(row=row, col=col) 
        self.typefunction    = typefunction  # String que define la funcion nativa a ejecutar
        self.parameters  = parameters        # Lista de parametros 
    def __str__(self):
        return f'<Native {self.typefunction} parameters: {self.parameters} >' 



    def execute(self, tree, table):
        if(len(self.parameters.var_node)==2):
            if(not(self.parameters.var_node[0] == "Int64" or self.parameters.var_node[0] == "Float64")):
                A = self.parameters.var_node[0].execute(tree,table)
            else:
                A = self.parameters.var_node[0]
            B = self.parameters.var_node[1].execute(tree,table)
            funcion = Nativa(A,B)
            return funcion.execute(self.typefunction)
        elif(len(self.parameters.var_node)==1):
            A = self.parameters.var_node[0].execute(tree,table)
            funcion = Nativa(A)
            return funcion.execute(self.typefunction)
        else:
            tree.addError(Description.SEMANTIC_EVAL_NATIVE,self.typefunction,self.row,self.col)
            return None

