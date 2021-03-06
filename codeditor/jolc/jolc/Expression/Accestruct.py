from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Array import AccesArray
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Error import *

class AccesStruct(Tree):
    def __init__(self,identifier,item, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.identifier = identifier        # Instancia de Identificador
        self.item = item                    # Identificador

    def __str__(self):
        return f'<AccesStruct id: {self.identifier} item:{self.item} >'

    '''
        El metodo de ejecucion busca el simbolo del struct y busca el miembro
        que se llamo, si existe devuelve su valor de lo contrario lanza error
    '''
    def execute(self, tree, table):
        valoriterable = table.lookup(self.identifier.identifier)           #Retorna el Simbolo
        if(len(self.item)>1):
            if valoriterable is not None and isinstance(valoriterable.value,dict) :                                      # Accedemos a los miembros
                for index in self.item[0:len(self.item)-1]:         
                    if index in valoriterable.value :                          # El valor es un miembro
                        valoriterable =  valoriterable.value[index]                      # Retornamos el valor del miembro
                    else:
                        tree.addError(Description.SEMANTIC_NO_MEMBER,self.item,self.row,self.col)      # Error el valor no es un miembro    
                if(self.item[len(self.item)-1] in valoriterable):
                    valoriterable = valoriterable[self.item[len(self.item)-1]]  
            else:                            
                tree.addError(Description.SEMANTIC_ID_404,self.identifier.identifier,self.row,self.col) 
        else:
            if valoriterable is not None and isinstance(valoriterable.value,dict) :                                      # Accedemos a los miembros     
                    if self.item[0] in valoriterable.value :                          # El valor es un miembro
                        valoriterable =  valoriterable.value[self.item[0]]                      # Retornamos el valor del miembro
                    else:
                        tree.addError(Description.SEMANTIC_NO_MEMBER,self.item,self.row,self.col)      # Error el valor no es un miembro    
            else:                            
                tree.addError(Description.SEMANTIC_ID_404,self.identifier.identifier,self.row,self.col) 
        return valoriterable
     
    
    def assignval(self,valor,tree,table):
        simbol = table.lookup(self.identifier.identifier)           #Retorna el Simbolo
        if simbol is not None:  
            if(isinstance(simbol.value,dict)):     
                if(simbol.mutabilidad or simbol.mutabilidad is None):                               # Accedemos a los miembros
                    if len(self.item) == 1 :
                        if self.item[0] in simbol.value: 
                            if(simbol.value[self.item[0]] == None):                         # El valor es un miembro
                                simbol.value[self.item[0]] = valor 
                            elif(type(simbol.value[self.item[0]]) == type(valor)):
                                simbol.value[self.item[0]] = valor       
                            else:   
                                tree.addError(Description.SEMANTIC_NOTYPE_MEMBER_ASIGN,self.item,self.row,self.col)             
                        else:
                            tree.addError(Description.SEMANTIC_NO_MEMBER,self.item,self.row,self.col)      # Error el valor no es un miembro  
                    else:
                        if simbol is not None and isinstance(simbol.value,dict) :                                      # Accedemos a los miembros
                            for index in self.item[0:len(self.item)-1]:         
                                if index in simbol.value :                          # El valor es un miembro
                                    simbol =  simbol.value[index]                      # Retornamos el valor del miembro
                                else:
                                    tree.addError(Description.SEMANTIC_NO_MEMBER,self.item,self.row,self.col)      # Error el valor no es un miembro    
                            simbol[self.item[len(self.item)-1]]  = valor
                        else:                            
                            tree.addError(Description.SEMANTIC_ID_404,self.identifier.identifier,self.row,self.col) 
                else:
                     tree.addError(Description.SEMANTIC_STRUCT_INMUTABLE,simbol.name,self.row,self.col)
            else:
                tree.addError(Description.SEMANTIC_STRUCT_NOINSTANACE,simbol.name,self.row,self.col)      # Error el valor no es un miembro    
        else:                            
            tree.addError(Description.SEMANTIC_ID_404,self.identifier.identifier,self.row,self.col) 
                