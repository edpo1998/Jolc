from io import TextIOWrapper
from os import name
from re import T
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Array import *
from codeditor.jolc.jolc.Expression.Accestruct import AccesStruct
from codeditor.jolc.jolc.Table.ScopedTable import *
from codeditor.jolc.jolc.Table.Symbol import *
from codeditor.jolc.jolc.Error import *

class Assignament(Tree):
    def __init__(self, left=None,tipo=None, right=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.left = left
        self.right = right
        self.tipo = tipo

    def __str__(self):
        return f'<Assignament id:{self.left} val: {self.right} >'

    def execute(self, tree, table):
        '''
            El valor que asignaremos a la nueva variable sin embargo es importante 
            validar los tipos de asignacion que definimos que puede recibir en
            la gramatica, debido a que recibe expression y puede recibir lo siguiente

            - Un valor primitivo (entero,decimal,cadena,caracter,booleano,None,)
            - Una Operacion unaria o binaria (booleana o aritmetica)
            - Una llamada a una funcion o bien puede ser asignacion de struct
            - Un arreglo como lista o como acceso
            - un identificador 
            - un acceso a un struct

            Todo lo anterior se reduce a las siguientes instacias de los valores devueltos:
                int,float,str,bool,list,dict,none

        '''
        valor = self.right.execute(tree,table)  # Valor de la asignacion

        if(isinstance(self.left,Identifier)):
        # SCOPE GLOBAL
            if isinstance(table,GlobalScope):
                if(isinstance(valor,dict)):
                    struct_name = self.left.identifier
                    struct_symbol = Var(name =struct_name,typedata= valor['Tipo'],row=self.row,col=self.col,value=valor['miembros'],mutabilidad = valor['mutable'])
                    struct_decl = table.lookup(struct_name, current_scope_only=True)
                    if struct_decl is None:
                        table.insert(struct_symbol) # Declaramos 
                    else:
                        # Asignamos un nuevo struct a la variable
                        if(struct_decl.mutabilidad is True):
                            struct_decl.value = valor['miembros']
                        else:
                            tree.addError(Description.SEMANTIC_STRUCT_INMUTABLE,struct_name,self.row,self.col)
                else:
                    var_name = self.left.identifier
                    tipo = None
                    if(isinstance(self.right,Array)) : 
                        tipo = self.right.type_data_array
                    var_symbol = Var(name=var_name, typedata= tipo,row=self.row,col=self.col,value=valor) 
                    vardecl = table.lookup(var_name, current_scope_only=True)
                    if vardecl is  None:
                        table.insert(var_symbol) #declaramos
                    else:
                       vardecl.value = valor    
        # SCOPE PARA FUNCIONES CON AMBITO HARD SCOPE     
            elif isinstance(table,FunctionScope) and table.scope_level == 2:
                if(isinstance(valor,dict)):
                    struct_name = self.left.identifier
                    if('Tipo' in  valor):
                        struct_symbol = Var(name =struct_name,typedata= valor['Tipo'],row=self.row,col=self.col,value=valor['miembros'],mutabilidad = valor['mutable'])
                        struct_decl = table.lookup(struct_name, current_scope_only=True)
                        if struct_decl is None:
                            table.insert(struct_symbol) # Declaramos 
                        else:
                            # Asignamos un nuevo struct a la variable
                            if(struct_decl.mutabilidad is True):
                                struct_decl.value = valor['miembros']
                            else:
                                tree.addError(Description.SEMANTIC_STRUCT_INMUTABLE,struct_name,self.row,self.col)
                    else:
                        struct_symbol = Var(name =struct_name,typedata= None,row=self.row,col=self.col,value=valor)
                        struct_decl = table.lookup(struct_name, current_scope_only=True)
                        if struct_decl is None:
                            table.insert(struct_symbol) # Declaramos 
                        else:
                             struct_decl.value = valor
                else:
                    var_name = self.left.identifier
                    if not(self.left.identifier in table.reference) :
                        var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=valor) 
                        vardecl = table.lookup(var_name, current_scope_only=True)
                        if vardecl is  None:
                            table.insert(var_symbol) #declaramos
                        else:
                            vardecl.value = valor 
                    else:
                        var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=valor) 
                        tree.global_scope.changeSymbol(var_symbol)
        # SCOPE PARA FUNCIONES ANIDADAS Y CICLOS       
            else: # Esta en una funcion anidada o un ciclo 
                if(isinstance(valor,dict)):
                    struct_name = self.left.identifier
                    if('Tipo' in  valor):
                        struct_symbol = Var(name =struct_name,typedata= valor['Tipo'],row=self.row,col=self.col,value=valor['miembros'],mutabilidad = valor['mutable'])
                        struct_decl = table.lookup(struct_name)
                        if struct_decl is None:
                            table.insert(struct_symbol) # Declaramos 
                        else:
                            # Asignamos un nuevo struct a la variable
                            if(struct_decl.mutabilidad is True):
                                struct_decl.value = valor['miembros']
                            else:
                                tree.addError(Description.SEMANTIC_STRUCT_INMUTABLE,struct_name,self.row,self.col)
                    else:
                        struct_symbol = Var(name =struct_name,typedata= None,row=self.row,col=self.col,value=valor)
                        struct_decl = table.lookup(struct_name)
                        if struct_decl is None:
                            table.insert(struct_symbol) # Declaramos 
                        else:
                             struct_decl.value = valor
                else:
                    var_name = self.left.identifier
                    if not(self.left.identifier in table.reference) :
                        var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=valor) 
                        vardecl = table.lookup(var_name)
                        if vardecl is  None:
                            table.insert(var_symbol) #declaramos
                        else:
                            vardecl.value = valor 
                    else:
                        var_symbol = Var(name=var_name, typedata= None,row=self.row,col=self.col,value=valor) 
                        tree.global_scope.changeSymbol(var_symbol)
        elif(isinstance(self.left,AccesArray)):
            self.left.assignValue(tree,table,valor);
        elif(isinstance(self.left,AccesStruct)):
            self.left.assignval(valor,tree,table)
        else:
            tree.addError(Description.SEMANTIC_INVALID_VAR,"invalid",self.row,self.col)