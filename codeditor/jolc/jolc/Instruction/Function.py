from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Table.ScopedTable import *
from codeditor.jolc.jolc.Table.Symbol import *
from codeditor.jolc.jolc.Error import *
from codeditor.jolc.jolc.Expression.Transferencia import *

class FunctionDecl(Tree):
    def __init__(self,func_name=None,formal_params=None,block_func =None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.func_name     = func_name      # Nombre de la funcion
        self.formal_params = formal_params  # Parametros (instancia de FormalParam)
        self.block_func    = block_func     # Cuerpo de la funcion (instancia de InstructionLIst)
        self.ref = None

    def __str__(self):
        return f'<Function name:{str(self.func_name)} parameters: {str(self.formal_params)}  body: {str(self.block_func)} >'

    def execute(self, tree, table):
        '''
            En la llamada a la funcion se declaro la nueva tabla de simbolos
            por lo tanto las instrucciones siguientes se realizaran en el ambito 
            de la funcion actual, es decir que la tabla se actualiza en cada llamada
        '''
        
        for instruction in self.block_func.declarations:    #Ejecucion de instrucciones
            ejecucion = instruction.execute(tree,table)
            # Sentencias de transferencia fuera de ciclo
            if isinstance(ejecucion, Break): 
                tree.addError(Description.SEMANTIC_TRANSFERENCE_LOCATION,instruction.__class__.__name__,instruction.row,instruction.col)
            elif isinstance(ejecucion, Continue): 
                tree.addError(Description.SEMANTIC_TRANSFERENCE_LOCATION,instruction.__class__.__name__,instruction.row,instruction.col)
            elif isinstance(ejecucion, Return):
                return ejecucion.result # Retorno del valor
        
      
