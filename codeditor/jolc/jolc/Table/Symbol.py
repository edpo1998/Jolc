'''
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   Simbolos permitidos en el Lenguaje de Programacion 'Jolc'    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█       Autor : Erick Daniel Poron Muñoz                                                      █
█       Fecha : 22/08/2021                                                                    █
█       Descripcion: Seran los simbolos almacenados en la tabla de simbolos                   █
█                                                                                             █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
'''

class Symbol:
    def __init__(self,name=None,typedata=None,row=None,col=None,mutabilidad=True):
        self.name        = name             # Nombre del simbolo
        self.typedata    = typedata         # Tipo de dato
        self.scope_level = 1                # Nivel de anidamiento por defecto global
        self.row         = row              # Linea 
        self.col         = col              # Columna
        self.mutabilidad = mutabilidad      # Valor que determina si un valor puede cambiar o no, se implemento y se utiliza unicamente en structs

    def __str__(self):
        return "<{class_name} name= {name} row= {row} col= {col}>".format(
                class_name = self.__class__.__name__,
                name       = self.name,
                row        = self.row,
                col        = self.col                
        )
    __repr__ = __str__




'''
    Simbolos que pueden ser primitivos,arreglos o estructuras
'''
class  Var(Symbol):
    def __init__(self,name=None,typedata=None,row=None,col=None, value=None, mutabilidad = True):
        super().__init__(name=name, typedata=typedata, row=row, col=col, mutabilidad=mutabilidad)
        self.value = value





'''
    Simbolo que representa una funcion
'''
class Function(Symbol):
    def __init__(self,name=None,typedata=None,row=None,col=None, members={}):
        super().__init__(name=name, typedata=typedata, row=row, col=col)
        self.formal_parameters = {}
        #Almacenaremos una referencia al nodo de sus instrucciones para efectos e implemetacion de un interprete por ejecucion en la pila
        #self. reference_sub_ast =None
        #Referencia a su tabla de simbolos


    

