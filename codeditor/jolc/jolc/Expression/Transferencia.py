from codeditor.jolc.jolc.Abstract.Node import Tree

#   Sentencias de Transferencia Return devuelve su instancia para controlar como devolver la expression
class Return(Tree):
    def __init__(self,expression=None,row = None, col =None):
        super().__init__(row=row, col=col)
        self.expression = expression

    def execute(self, tree, table):
        self.result = self.expression.execute(tree,table)
        return self

    def __str__(self):
        return f'<Return ex: {self.expression} >'

# Sentencia de Transferencia Continue, devuelve su instancia para poder manejar el error o ejecucion
class Continue(Tree):
    def __init__(self, row=None, col=None):
        super().__init__(row=row, col=col)
    def __str__(self):
        return f'<Continue >'

    def execute(self, tree, table):
        return self


# Sentencia de Transferencia Break, devuelve su instancia para poder manejar el error o ejecucion
class Break(Tree):
    def __init__(self, row=None, col=None):
        super().__init__(row=row, col=col)

    def execute(self, tree, table):
        return self

    def __str__(self):
        return f'<Break >'