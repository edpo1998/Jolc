from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Instruction.Assignament import Assignament
from codeditor.jolc.jolc.Table.ScopedTable import *
from codeditor.jolc.jolc.Table.Symbol import *
from codeditor.jolc.jolc.Error import *


class Definition(Tree):
    def __init__(self, valScope=None, expression=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.valScope = valScope        # Valor del entorno a definir
        self.expression = expression    # Id o Assignament
    def __str__(self):
        return f'<Definition scope:{self.valScope} expression: {self.expression} >'

    def execute(self, tree, table):
        entornodcl = self.valScope        # local o global
        variable   = self.expression      # puede ser declaracion o asignacion
        
        if(entornodcl == 'global'):
            if(isinstance(table,GlobalScope)): #Error al utilizar global en el ambito Global
                tree.addError(Description.SEMANTIC_GLOBAL_GLOBAL,'global',self.row,self.col)
            else:
                # Crear Referencia a la variable global
                # Si no es el ambito global entonces puedo crear referencias en cualquier ambito
                if(isinstance(variable,Identifier)): # Restringir a unicamente un identificador
                    # Verificar Redeclaracion de la referencia
                    if(variable.identifier in  table.reference ):
                        if(not(isinstance(table,CicloFor) or isinstance(table,CicloWhile))):
                            tree.addError(Description.SEMANTIC_GLOBAL_RDCL,variable.identifier,self.row,self.col)
                    else: 
                        # Almacenamos el nombre del simbolo como referencia
                        # Verificamos que exista en el ambito global
                        if(variable.identifier in tree.global_scope.symbols):
                            table.reference.append(variable.identifier) #Ingresamos el apuntador
                        else:
                            tree.addError(Description.SEMANTIC_REF_NOGLOBAL,variable.identifier,self.row,self.col) 
                elif(isinstance(variable,Assignament)):
                      if(isinstance(variable.left,Identifier)): # Restringir a unicamente un identificador
                        # Verificar Redeclaracion de la referencia
                        if(variable.left.identifier in  table.reference ):
                            if(not(isinstance(table,CicloFor) or isinstance(table,CicloWhile))):
                                tree.addError(Description.SEMANTIC_GLOBAL_RDCL,variable.identifier,self.row,self.col)
                            tree.global_scope.lookup(variable.left.identifier).value = variable.right.execute(tree,table)
                        else: 
                            # Almacenamos el nombre del simbolo como referencia
                            # Verificamos que exista en el ambito global
                            if(variable.left.identifier in tree.global_scope.symbols):
                                table.reference.append(variable.left.identifier) #Ingresamos el apuntador
                                tree.global_scope.lookup(variable.left.identifier).value = variable.right.execute(tree,table)
                            else:
                                tree.addError(Description.SEMANTIC_REF_NOGLOBAL,variable.identifier,self.row,self.col)   
                else:                    
                    tree.addError(Description.SEMANTIC_NODECL_GLOBAL,"Declaracion Global",self.row,self.col)
        # La definicion es Local
        else:
            if(isinstance(variable,Identifier)): # Al asignar un valor de eso se encargara assignament por aparte
                var_name = variable.identifier
                var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=None)
                # Validamos que no se haya declarado ya en caso de estar en un nivel de ambito 2
                vardecl = table.lookup(var_name, current_scope_only=True)     
                if vardecl is  None:
                    table.insert(var_symbol) # declaramos ya que no existe en el ambito tendra valor None
                else:
                    if(not(isinstance(table,CicloFor) or isinstance(table,CicloWhile))):
                        tree.addError(Description.SEMANTIC_ID_DUPLICATE,var_name,self.row,self.col)
            elif(isinstance(variable,Assignament)):
                var_name = variable.left.identifier
                var_val = variable.right.execute(tree,table)
                var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=var_val)
                # Validamos que no se haya declarado ya en caso de estar en un nivel de ambito 2
                vardecl = table.lookup(var_name, current_scope_only=True)     
                if vardecl is  None:
                    table.insert(var_symbol) # declaramos ya que no existe en el ambito tendra valor None
                else:
                    if(not(isinstance(table,CicloFor) or isinstance(table,CicloWhile))):
                        tree.addError(Description.SEMANTIC_ID_DUPLICATE,var_name,self.row,self.col)
                    table.insert(var_symbol) # sustituir 
            else:                    
                    tree.addError(Description.SEMANTIC_NODECL_GLOBAL,"Declaracion Global",self.row,self.col) 