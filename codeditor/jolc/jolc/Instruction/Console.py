from codeditor.jolc.jolc.Abstract.Node import Tree

class ShowConsole(Tree):
    def __init__(self,expression=None,nextline = False, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.expression = expression
        self.nextline = nextline
    def __str__(self):
        return f'<ShowConsole  value: {self.expression} >'
        
    '''
        Concatena la lista de expresiones que se quiere imprimir
        println(exp1,exp2,exp3,..);
        print(exp1,exp2,exp3,..);
    '''
    def execute(self, tree, table):
        cadena = ""
        for val in self.expression.var_node :
            cadena = cadena + str(val.execute(tree,table))
        cadena = cadena + "\n" if self.nextline else cadena
        tree.addConsole(cadena);