from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Table.ScopedTable import CicloFor
from codeditor.jolc.jolc.Expression.Array import Array, Container,Slice,AccesArray
from codeditor.jolc.jolc.Expression.Primitive import ValString
from codeditor.jolc.jolc.Expression.Transferencia import Return,Break,Continue
from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Table.Symbol import Var
class For(Tree):
    def __init__(self, iterable=None, instructions=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.iterable = iterable
        self.instructions = instructions
    
    def __str__(self):
        return f'<For iterable: {self.iterable} instrucciones: {self.instructions} >'

    def execute(self, tree, table):
       
        for_scope = CicloFor(
                    scope_name          = table.scope_name + '_for',                       # Nombre del ambito
                    scope_level         = table.scope_level + 1,    # Nivel de Anidacion sera el siguiente de su predecesor
                    enclosing_scope     = table,                    # Referencia al ambito superior en el que anida
                )

        if(isinstance(self.iterable,Container)):
            # Ingresamos la variable pivote a iterar\
            pivote = Var(name=self.iterable.item,typedata=None,row=self.row,col=self.col,value=None)
            for_scope.insert(pivote)

            # Evaluamos el container
            iterable = self.iterable.container
            #print(iterable)
            if isinstance(iterable,Slice):
                rango = iterable.execute(tree,table)
                if(rango['start'] is None or rango['end'] is None):
                    tree.addError(Description.SEMANTIC_NON_RANGE,'for',self.row,self.col)
                else:
                    for pivote.value in range(rango['start'],rango['end']+1):
                        for instruccion in self.instructions.declarations:
                            result = instruccion.execute(tree,for_scope)
                            if(isinstance(result,Break)):  return None
                            if(isinstance(result,Return)): return result
                            if(isinstance(result,Continue)): continue
            elif isinstance(iterable, AccesArray):
                rango = iterable.execute(tree,table)
                if(isinstance(rango,list)):
                    for pivote.value in rango:
                        for instruccion in self.instructions.declarations:
                            result = instruccion.execute(tree,for_scope)
                            if(isinstance(result,Break)):  return None
                            if(isinstance(result,Return)): return result
                            if(isinstance(result,Continue)): continue
                else:
                  tree.addError(Description.SEMANTIC_NON_ITERABLE,iterable.identifier,self.row,self.col)
            elif isinstance(iterable,ValString):
                rango = iterable.execute(tree,table)
                for pivote.value in rango:
                    for instruccion in self.instructions.declarations:
                        result = instruccion.execute(tree,for_scope)
                        if(isinstance(result,Break)):  return None
                        if(isinstance(result,Return)): return result
                        if(isinstance(result,Continue)): continue
            elif  isinstance(iterable,Identifier):
                rango = iterable.execute(tree,table)
                if(isinstance(rango,list) or isinstance(rango,dict) or isinstance(rango,str)):
                    for pivote.value in rango:
                        for instruccion in self.instructions.declarations:
                            result = instruccion.execute(tree,for_scope)
                            if(isinstance(result,Break)):  return None
                            if(isinstance(result,Return)): return result
                            if(isinstance(result,Continue)): continue
                else:
                  tree.addError(Description.SEMANTIC_NON_ITERABLE,iterable.identifier,self.row,self.col)  
            elif isinstance(iterable,Array):
                rango = iterable.execute(tree,table)
                for pivote.value in rango:
                        for instruccion in self.instructions.declarations:
                            result = instruccion.execute(tree,for_scope)
                            if(isinstance(result,Break)):  return None
                            if(isinstance(result,Return)): return result
                            if(isinstance(result,Continue)): continue
            else:
                tree.addError(Description.SEMANTIC_NON_ITERABLE,'for',self.row,self.col)
        else:
             tree.addError(Description.SEMANTIC_FOR_NONVALIDAD_EXP,'for',self.row,self.col)
