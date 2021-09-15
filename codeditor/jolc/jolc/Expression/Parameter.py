from codeditor.jolc.jolc.Abstract.Node import Tree

'''
    Realmente pudimos tratar una lista en la generacion del ast
    pero esta clase nos servira para graficar el arbol
'''
class FormalParam(Tree):
    def __init__(self, var_node = [],row = None, col =None):
        super().__init__(row=row, col=col)
        self.var_node = var_node

    def execute(self, tree, table):
        return self
    
    def __str__(self):
        parameters = ''.join(map(str, self.var_node))
        return f'<FormalParam parametros: {str(parameters)} >'


