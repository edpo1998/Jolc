from codeditor.jolc.jolc.Expression.Array import Slice
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Error import Description
# Clase de la que derivan los valores primitivos
class Primitive(Tree):
    def __init__(self,value=None,row = None, col =None):
        super().__init__(row=row, col=col)
        self.value = value
        self.row   = row
        self.col   = col

# Es un numero entero   
class ValInteger(Primitive):
    def __init__(self, value=None, row=None, col=None):
        super().__init__(value=value, row=row, col=col)

    def execute(self, tree, table):
        return int(self.value)

    def __str__(self):
        return f'<ValInteger val: {self.value} >'

# Es un numero decimal
class ValFloat(Primitive):
    pass

    def execute(self, tree, table):
        return float(self.value)

    def __str__(self):
        return f'<ValFloat val: {self.value} >'


# Es una cadena
class ValString(Primitive):
    def __init__(self, value=None, row=None, col=None,rango=None):
        super().__init__(value=value, row=row, col=col)
        self.rango = rango

    def execute(self, tree, table):
         if(self.rango is None):
          return str(self.value)
         else:
            if(isinstance(self.rango,Slice)):
                pedazostr = self.rango.execute( tree, table)
                if(pedazostr['start'] is None and pedazostr['end'] is None ):
                    return str(self.value)
                elif(pedazostr['start'] is None): 
                    if(pedazostr['end'] <= len(self.value)):
                        return str(self.value)[:pedazostr['end']]
                    else:
                        tree.addError(Description.SEMANTIC_NON_LENGHT_CADENA,str(self.value),self.row,self.col)
                elif(pedazostr['end'] is None):    # Crep que deberia ser error
                    if(len(self.value)>=pedazostr['start']):
                        return str(self.value)[pedazostr['start']-1:]
                    else:
                        tree.addError(Description.SEMANTIC_NON_LENGHT_CADENA,str(self.value),self.row,self.col)
                else:
                    if(len(self.value)>=pedazostr['start'] and pedazostr['end'] <= len(self.value)):
                        return str(self.value)[pedazostr['start']-1:pedazostr['end']]      
                    else:
                        tree.addError(Description.SEMANTIC_NON_LENGHT_CADENA,str(self.value),self.row,self.col)
            else:
                index = self.rango.execute(tree,table)
                if(isinstance(index,int)):
                    return self.value[index-1]
                else:
                     tree.addError(Description.SEMANTIC_INDEX_NO_INT,str(self.value),self.row,self.col)
                    

    def __str__(self):
        return f'<ValString val: {self.value} >'

# Es un caracter pero lo trataremos como cadena para efectos de python
class ValCaracter(Primitive):
    def __init__(self, value=None, row=None, col=None):
        super().__init__(value=value, row=row, col=col)
    def execute(self, tree, table):
        return str(self.value)
    def __str__(self):
        return f'<ValCaracter val: {self.value} >'

# Valor Booleano 
class ValBool(Primitive):
    def __init__(self, value=None, row=None, col=None):
        super().__init__(value=value, row=row, col=col)

    def execute(self, tree, table):
        return bool(self.value)

    def __str__(self):
        return f'<ValBool val: {self.value} >'

# Valor nulo
class ValNothing(Primitive):
    def __init__(self, value=None, row=None, col=None):
        super().__init__(value=value, row=row, col=col)
    
    def execute(self, tree, table):
        return None

    def __str__(self):
        return f'<valNothing val: {self.value} >'