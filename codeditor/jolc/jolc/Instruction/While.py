from codeditor.jolc.jolc.Expression.Transferencia import Break, Continue, Return
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Table.ScopedTable import CicloWhile
from codeditor.jolc.jolc.Error import Description

class While(Tree):
    
    def __init__(self, condition=None, instructions=None,row=None,col=None):
        super().__init__(row=row, col=col)
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return f'<While condition: {self.condition} instrucciones: {self.instructions} >'
    
    def execute(self, tree, table):
        while_scope = CicloWhile(
                    scope_name          = table.scope_name + '_while',              # Nombre del ambito
                    scope_level         = table.scope_level + 1,                    # Nivel de Anidacion sera el siguiente de su predecesor
                    enclosing_scope     = table,                                    # Referencia al ambito superior en el que anida
                )
        
        while True:
            condicion = self.condition.execute(tree,table)
            if(isinstance(condicion,bool)):
                if(condicion):
                    for instruccion in self.instructions.declarations:
                        result = instruccion.execute(tree,while_scope)
                        if(isinstance(result,Break)):  return None
                        if(isinstance(result,Return)): return result
                        if(isinstance(result,Continue)): continue
                else:
                    break
            else:
                tree.addError(Description.SEMANTIC_EVAL_TBUNARY,'while',self.row,self.col)
            
    

    
        