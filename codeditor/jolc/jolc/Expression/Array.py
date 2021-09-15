
from typing import Iterable
from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.EnvNative import FuncNative as Nativa

class Array(Tree):

    def __init__(self,items=None, type_data_array=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.items = items                      # Items del arreglo
        self.type_data_array = type_data_array  # Verifica que se defina un tipo de dato para la evaluacion
    
    def __str__(self):
        return f'<Array items:{self.items} type = {self.type_data_array}>'
    
    '''
        Execute genera el arreglo a almacenar en el simbolo
        es posible restringir el arreglo unicamente a un tipo de dato 
        durante su asignacion, el metodo returna un arreglo vacio 
        o bien un arreglo con los datos ingresados
    '''
    def execute(self, tree, table):
        new_array = []

        if(self.type_data_array is None):       # No se Realizan validacion de tipos
            # Iterar items del arreglo
            for item in self.items.var_node:
                val = item.execute(tree,table)
                new_array.append(val)
        else:   # [...] Array{ TipoDato }         Se validan tipos
            for item in self.items.var_node:
                val = item.execute(tree,table)
                if(isinstance(val,int) and self.type_data_array == 'Int64'):
                    new_array.append(val)
                elif(isinstance(val,float) and self.type_data_array == 'Float64'):
                    new_array.append(val)
                elif(isinstance(val,str) and self.type_data_array == 'String'):
                    new_array.append(val)
                elif(isinstance(val,str) and self.type_data_array == 'Char'):
                    new_array.append(val)
                elif(isinstance(val,bool) and self.type_data_array == 'Bool'):
                    new_array.append(val)
                else:
                    tree.addError(Description.SEMANTIC_ASSIG_ARRAY,str(val),self.row,self.col)
     # Retornara los valores validos, si ninguno es valido entonces el arreglo se declara como vacio
     # Sin embargo se alertara de los valores no aceptados 
        return new_array   # Es una lista

'''
    Devuelve un diccionario con los valores del rango con las keys
    start y end
'''

class Slice(Tree):
    def __init__(self,startslice=None,endslice=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.startslice = startslice
        self.endslice = endslice
        
    def execute(self, tree, table):
        start = None
        end = None
        if (self.startslice is None and self.endslice is None):
            pass
        elif(self.startslice is None):
            end = self.endslice.execute(tree,table)
        elif(self.endslice is None):
            start = self.startslice.execute(tree,table)
        else:
            start = self.startslice.execute(tree,table)
            end = self.endslice.execute(tree,table)
        return {'start':start,'end':end}
    def __str__(self):
        return f'<Slice start: {self.startslice} end:{self.endslice} >'


class AccesArray(Tree):
    def __init__(self,identifier,items=[], row=None,col=None):
        super().__init__(row=row, col=col) 
        self.identifier = identifier    # Identificador Explicito
        self.items = items              # Items es un arreglo de valores index
                                         # Puede ser id[n-2][n-1].....[n]
    def __str__(self):
        return f'<AccesArray id: {self.identifier} item:{self.items} >'
    '''
    
    '''
    def execute(self, tree, table):
        symarray = table.lookup(self.identifier)
        countindex = len(self.items)    # Numero de Indices a iterar
        if(symarray is None):
            tree.addError(Description.SEMANTIC_ARRAY_404,self.identifier,self.row,self.col)
        else:
            valoriterable = symarray.value  # Lista de valores del arreglo
            if(isinstance( self.items[0],Slice)):
                pedazo = self.items[0].execute(tree,table)
                if(pedazo['start'] is None and pedazo['end'] is None ):
                    return valoriterable[:]
                elif(pedazo['start'] is None):  #Creo que deberia devolver unicamente 1 valor
                    if(pedazo['end'] <= len(valoriterable)):
                        return valoriterable[:pedazo['end']]
                    else:
                         tree.addError(Description.SEMANTIC_LENG_ARRAY,str(" Inddice Final"),self.row,self.col)
                elif(pedazo['end'] is None):    # Crep que deberia ser error
                    if(len(valoriterable)>=pedazo['start']):
                        return valoriterable[pedazo['start']-1:]
                    else:
                        tree.addError(Description.SEMANTIC_LENG_ARRAY,str(" Indice Inicial"),self.row,self.col)
                else:
                    if(len(valoriterable)>=pedazo['start'] and pedazo['end'] <= len(valoriterable)):
                        return valoriterable[pedazo['start']-1:pedazo['end']]      
                    else:
                        tree.addError(Description.SEMANTIC_LENG_ARRAY,str("Algun Indice"),self.row,self.col)
            else:
                for index in self.items:
                    valoriterable = self.returnArr(tree,valoriterable,index.execute(tree,table)) 

                return valoriterable 

    def access_struct_array(self, tree, table ,array_list):
        countindex = len(array_list)
        valoriterable = array_list
        if(isinstance( self.items[0],Slice)):
            pedazo = self.items[0].execute(tree,table)
            if(pedazo['start'] is None and pedazo['end'] is None ):
                return valoriterable[:]
            elif(pedazo['start'] is None):  #Creo que deberia devolver unicamente 1 valor
                if(pedazo['end'] <= len(valoriterable)):
                    return valoriterable[:pedazo['end']]
                else:
                    tree.addError(Description.SEMANTIC_LENG_ARRAY,str(" Inddice Final"),self.row,self.col)
            elif(pedazo['end'] is None):    # Crep que deberia ser error
                if(len(valoriterable)>=pedazo['start']):
                    return valoriterable[pedazo['start']-1:]
                else:
                    tree.addError(Description.SEMANTIC_LENG_ARRAY,str(" Indice Inicial"),self.row,self.col)
            else:
                if(len(valoriterable)>=pedazo['start'] and pedazo['end'] <= len(valoriterable)):
                    return valoriterable[pedazo['start']-1:pedazo['end']]      
                else:
                    tree.addError(Description.SEMANTIC_LENG_ARRAY,str("Algun Indice"),self.row,self.col)
        else:
            for index in self.items:
                valoriterable = self.returnArr(tree,valoriterable,index.execute(tree,table)) 
            return valoriterable 

    def assignValue(self,tree,table,value):
        symarray = table.lookup(self.identifier)
        countindex = len(self.items)    # Numero de Indices a iterar
        if(symarray is None):
            tree.addError(Description.SEMANTIC_ARRAY_404,self.identifier,self.row,self.col)
            return None
        else:
            valoriterable = symarray.value  # Lista de valores del arreglo
            if(isinstance(valoriterable,list)):
                if(isinstance( self.items[0],Slice)):
                    tree.addError(Description.SEMANTIC_VALORNOACCES,self.identifier,self.row,self.col)
                    return None
                else:
                    '''
                        arreglo[]   si hay solo uno devolver ese indice
                        arreglo[][] si hay mas de un indice iterar hasta n-1
                    '''
                    if(countindex>1):
                        for index in self.items[0:countindex-1]:
                            valoriterable = self.returnArr(tree,valoriterable,index.execute(tree,table))  # los extrae recursivamente
                        indice = self.items[countindex-1].execute(tree,table) #Es el ultimo valor que tendra como indice
                        #Devolver lo que contenga el ultimo index
                        if(isinstance(indice,int)):
                            if(symarray.typedata is None):
                                valoriterable[indice-1] = value
                            else:
                                if(isinstance(value,int) and symarray.typedata == 'Int64'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Float64'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'String'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Char'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Boolean'):
                                    valoriterable[indice-1] = value
                                else:
                                    tree.addError(Description.SEMANTIC_TYPE_ARREGLO,self.identifier,self.row,self.col)
                        else:
                             tree.addError(Description.SEMANTIC_INDEX_NO_INT,self.identifier,self.row,self.col)
                    else:
                        indice = self.items[0].execute(tree,table)
                        if(isinstance(indice,int)):
                            if(symarray.typedata is None):
                                valoriterable[indice-1] = value
                            else:
                                if(isinstance(value,int) and symarray.typedata == 'Int64'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Float64'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'String'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Char'):
                                    valoriterable[indice-1] = value
                                elif(isinstance(value,int) and symarray.typedata == 'Boolean'):
                                    valoriterable[indice-1] = value
                                else:
                                    tree.addError(Description.SEMANTIC_TYPE_ARREGLO,self.identifier,self.row,self.col)
                        else:
                             tree.addError(Description.SEMANTIC_INDEX_NO_INT,self.identifier,self.row,self.col)
            else:
                tree.addError(Description.SEMANTIC_NOITERABLE,self.identifier,self.row,self.col)
                    
    def returnArr(self,tree,array,indexjulia):
        index =  indexjulia - 1
        if(isinstance(array,list) and len(array)>=indexjulia): # Julia accede con el numero real del elemento
                return array[index] # Aca ya accedemos con el valor que empieza desde 0
        else:
            tree.addError(Description.SEMANTIC_LENG_ARRAY,str("Lenght"),self.row,self.col)#Generar error de Longitud o de que no es un arreglo
            return None       




class Container(Tree):
    def __init__(self,item=None,container=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.item = item
        self.container = container
    
    def __str__(self):
        return f'<Container item: {self.item} container:{self.container} >'

    def execute(self, tree, table):
        valor = self.item.execute(tree,table)   #Variable local a crear en el ambito del for
        rango = self.container #Puede ser los siguientes Iterables: cadena,slice,arreglo,struct
        return {
            'val': valor,
            'rango' : rango
        }


'''
    Estas clases sirven para realizar operaciones a arreglos por medio del operador punto
    se implemento sin embargo fue retirado de los alcances del proyecto

'''
class operatorArray(Tree):
    def __init__(self,op=None,exp=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.op = op
        self.exp = exp

class OperationNativeArray(Tree):
    def __init__(self,tiponative=None,array_access=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.tiponative = tiponative
        self.array_access = array_access
    def execute(self, tree, table):
        iterable = self.array_access.execute(tree,table)
        
        for idx, val in enumerate(iterable):
            nativeitem = Nativa(val)
            iterable[idx] = nativeitem.execute(self.tiponative) 

        return iterable

class OperationArArray(Tree):
    def __init__(self,operator=None,array_access=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.operator = operator
        self.array_access = array_access

    def execute(self, tree, table):
        iterable = self.array_access.execute(tree,table)
        if(isinstance(iterable,list)):
            operator = self.operator.op
            valor = self.operator.exp.execute(tree,table)
            if(operator == '+'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val + valor
            elif(operator == '-'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val - valor
            elif(operator == '*'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val * valor
            elif(operator == '/'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val / valor
            elif(operator == '%'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val % valor
            elif(operator == '^'):
                for idx, val in enumerate(iterable):
                    iterable[idx] = val ** valor
            return iterable
        else:
             tree.addError(Description.SEMANTIC_NON_ITERABLE,"Array",self.row,self.col)