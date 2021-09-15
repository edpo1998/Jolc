from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.Operation import Boolean
from codeditor.jolc.jolc.Expression.Primitive import ValBool
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Transferencia import *
from codeditor.jolc.jolc.Error import *

'''
    Este bloque nos sirve para poder derivar un bloque condicional
    y agregar caracteristicas diferentes al IF
'''
class BlockConditional(Tree):
    def __init__(self,condition=None,instructions=None,row=None,col=None):
        super().__init__(row=row,col=col)
        self.condition = condition
        self.instructions = instructions


'''
        BLOQUE IF GENERAL

'''
class If(BlockConditional):
    def __init__(self, condition = None, instructions = None,alternatives=None,nomatches_instruction=None,row =None,col =None):
        super().__init__(condition=condition, instructions=instructions,row =row,col=row)
        if alternatives is None:
            alternatives = []
        self.alternatives = alternatives
        self.nomatches_instruction = nomatches_instruction

    def __str__(self):
       altr = ''.join(map(str,self.alternatives))
       return f'<If condition: {str(self.condition)} alternatives: {altr} nomatch: {str(self.nomatches_instruction)} >'
    def execute(self, tree, table):
            condicion = self.condition.execute(tree,table)  # Recibe el valor
            if not(isinstance(condicion,bool)) : #Debe retornar un valor booleano
                tree.addError(Description.SEMANTIC_NOBOOL,str(condicion),self.row,self.col)    #Generar Error
                return None
            # Ejecutar If
            if(bool(condicion) == True):
                for instruction in self.instructions.declarations:
                    ejecucion = instruction.execute(tree,table) 
                    if isinstance(ejecucion, Break): 
                        return ejecucion                    # Debo validar si estoy en ciclo
                    elif isinstance(ejecucion, Continue): 
                        return ejecucion                    # Debo validar si estoy en ciclo
                    elif isinstance(ejecucion, Return):
                        return ejecucion                  
            else:
                nomatch = True
                if(len(self.alternatives)>0):
                    for elseif in self.alternatives:
                        if(elseif.execute(tree,table)): #Si ya ejecuto un if corta el flujo 
                            for instruction in elseif.instructions.declarations:
                                ejecucionelseif = instruction.execute(tree,table) 
                                if isinstance(ejecucionelseif, Break): 
                                    return ejecucionelseif                    # Debo validar si estoy en ciclo
                                elif isinstance(ejecucionelseif, Continue): 
                                    return ejecucionelseif                    # Debo validar si estoy en ciclo
                                elif isinstance(ejecucionelseif, Return):
                                    return ejecucionelseif
                            nomatch = False
                            break
                # Si se ejecuto un elseif no entra aca
                if(nomatch and self.nomatches_instruction is not None):    # Debido a que no se realizo ninguna sentencia de verdad
                    for instruction in self.nomatches_instruction.declarations:
                        ejecucion = instruction.execute(tree,table)
                        if isinstance(ejecucion, Break): 
                           return ejecucion                     # Debo validar si estoy en ciclo
                        elif isinstance(ejecucion, Continue): 
                            return ejecucion                    # Debo validar si estoy en ciclo
                        elif isinstance(ejecucion, Return):
                            return ejecucion

        
class ElseIf(BlockConditional):
    def __init__(self, condition, instructions, row, col):
        super().__init__(condition=condition, instructions=instructions, row=row, col=col)
        
    def __str__(self):
       return f'<ElseIf condition: {self.condition} instrucciones: {self.instructions} >'

    def execute(self, tree, table):
            condicion = self.condition.execute(tree,table) 

            if not(isinstance(condicion,bool)) : #Debe retornar un valor booleano
                tree.addError(Description.SEMANTIC_NOBOOL,str(condicion),self.row,self.col)    #Generar Error
                return None

            if(bool(condicion) == True):
                return True
            else:
                return False