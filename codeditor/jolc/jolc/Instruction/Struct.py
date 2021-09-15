from codeditor.jolc.jolc.Table.ScopedTable import GlobalScope
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Evaluacion import EvalType
from codeditor.jolc.jolc.Error import Description

class Struct(Tree):
    def __init__(self,identifier=None,members=None,mutable=True,row=None,col=None):
        super().__init__(row=row, col=col) 
        self.identifier = identifier    # Nombre del tda
        self.members = members          # Miembros  (Instancia de FormalParam)
        self.mutable = mutable          # Valor Booleano de mutabilidad 
    def __str__(self):
        return f'<Struct const: {str(self.mutable)} id: {self.identifier} members: {self.members} >'

    def execute(self, tree, table):
        if(isinstance(table,GlobalScope)):  #Solo se pueden declarar en el ambito global
            tdaname = self.identifier
            tdamembers = {}
            tdamembers['mutable'] = self.mutable
            if(not(tdaname in tree.tda)):   # El struct no debe estar redeclarado
                # Extraemos los miembros
                for miembro in self.members.var_node :  #node.members es una instancia de FormalParam
                    # Colocamos instancias de tipos primitivos para poder validar el valor segun el valor del miembro
                    if(isinstance(miembro,Identifier)): # No posee  tipo definido
                        tdamembers[str(miembro.identifier)] = None # member:None
                    elif(isinstance(miembro,EvalType)): # Posee tipo definido a evaluar
                        if(miembro.type_data == 'Int64'):
                            tdamembers[str(miembro.expression.identifier)] = int# member:int
                        elif(miembro.type_data == 'Float64'):
                            tdamembers[str(miembro.expression.identifier)] = float#  member:float
                        elif(miembro.type_data == 'String' or miembro.type_data == 'Char'):    
                            tdamembers[str(miembro.expression.identifier)] = str#  member:str
                        elif(miembro.type_data == 'Bool'):
                            tdamembers[str(miembro.expression.identifier)] = bool#  member:bool
                        else:
                            tree.addError(Description.SEMANTIC_DECL_STRUCT,str(miembro.type_data),self.row,self.col)
                tree.tda[tdaname] = tdamembers
            else:
                tree.addError(Description.SEMANTIC_STRUCT_RDECL,tdaname,self.rowm,self.col)
        else:
            tree.addError(Description.SEMANTIC_DECL_STRUCT,self.identifier,self.row,self.col) # Solo se pueden crear TDAs en el ambito Global   
        