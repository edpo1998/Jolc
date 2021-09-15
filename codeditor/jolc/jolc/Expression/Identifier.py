from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Table.ScopedTable import GlobalScope

class Identifier(Tree):
    def __init__(self,identifier, row=None,col=None):
        super().__init__( row=row,col=col)
        self.identifier = identifier

    def __str__(self):
        return f'< Identifier name: {self.identifier} >'
    '''
        getSymb : Devuelve un simbolo
        execute:  Devuelve el valor del simbolo
        changevalue: cambia el valor del simbolo
    '''
    def getSymb(self, tree, table):
        '''
            De no estar en un ambito global damos precedencia a las referencias
            para evitar conflictos 
        '''
        if(isinstance(table,GlobalScope) == False):  # Es un ambito de nivel 2 o mayor
            if not(self.identifier in table.reference):
                '''
                    Si no esta en las referencias buscar recursivamente
                '''
                symb = table.lookup(self.identifier)
                # Devovler error si no lo encuentra
                if symb is None:
                    tree.addError(Description.SEMANTIC_ID_404,self.identifier,self.row,self.col)
                    return None

                # El simbolo contiene algun valor y no es una referencia
                return symb
            else:
                # De estar en las referencias devolvemos el simbolo del ambito global
                return tree.global_scope.symbols[self.identifier]  
        else:
            '''
                Debido a que se encuentra en el ambito global
                devolver unicamente los valores declarados dentro de el
            '''
            symb = tree.global_scope.lookup(self.identifier)
            # El simbolo puede ser una variable,arreglo o estructura
            if symb is None:
                tree.addError(Description.SEMANTIC_ID_404,self.identifier,self.row,self.col)
                return None
            return symb

    def changevalue(self,tree,table,value):
        sym = table.lookup(self.identifier)
        sym.value = value

    def execute(self, tree, table):
        '''
            De no estar en un ambito global damos precedencia a las referencias
            para evitar conflictos 
        '''
        if(isinstance(table,GlobalScope) == False):
            if not(self.identifier in table.reference):
                '''
                    Si no esta en las referencias buscar recursivamente
                '''
                symb = table.lookup(self.identifier)
                # Devovler error si no lo encuentra
                if symb is None:
                    tree.addError(Description.SEMANTIC_ID_404,self.identifier,self.row,self.col)
                    return None

                # El simbolo contiene algun valor y no es una referencia
                return symb.value
            else:
                # De estar en las referencias devolvemos el valor global puede ser de cualquier tipo
                return tree.global_scope.symbols[self.identifier].value 
        else:
            '''
                Debido a que se encuentra en el ambito global
                devolver unicamente los valores declarados dentro de el
            '''
            symb = tree.global_scope.lookup(self.identifier)
            # El simbolo puede ser una variable,arreglo o estructura
            if symb is None:
                tree.addError(Description.SEMANTIC_ID_404,self.identifier,self.row,self.col)
                return None
            return symb.value
    
