from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Table.ScopedTable import GlobalScope
from codeditor.jolc.jolc.Error import *

class EvalType(Tree):
    def __init__(self, expression=None, type_data=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.expression = expression    # Expresion ser lo que sea siempre y cuando devuelva un valor
        self.type_data = type_data      # Tipo de Dato puede ser Sturct o Primitivo
    def __str__(self):
        return f'<EvalType exp:{self.expression} type_Data: {str(self.type_data)} >'

    def getStruct(self,nombre,tipo,tree, table):
        symb = table.lookup(nombre)
        if(symb.typedata == tipo):
            return symb
        else:
            tree.addError(Description.SEMANTIC_TDA_NO_COINCIDE,tipo,self.row,self.col) 
            return None

    def execute(self, tree, table):
        '''
            Expresion puede ser lo que sea siempre y cuando devuelva un valor
            los arreglos y structs los veremos por aparte, asi que
            sea lo que sea tiene que devolver un tipo de dato primitivo  ya que
            los que no poseen tipo (None) no se definen asi expresion::tipo
            si no solamente la varibale
        '''
        valor = self.expression.execute(tree,table) #Verificar Tipo de dato
        if(isinstance(valor,int)==True and str(self.type_data) == 'Int64'):
            return valor
        elif(isinstance(valor,float)==True  and str(self.type_data) == 'Float64'):
            return valor
        elif(isinstance(valor,str)==True  and (str(self.type_data) == 'String' or str(self.type_data) == 'Char')):    
            return valor
        elif(isinstance(valor,bool)==True  and str(self.type_data) == 'Bool'):
            return valor
        else: # Es por eso que retorno error ya que no es algo que pueda asignarsele un valor
            tree.addError(Description.SEMANTIC_ASSIG_NOTYPE,str(valor),self.row,self.col)
        # El valor asignado a la varible sera None
        # Por la tanto puede ocurrir que se encadenen errores o bien
        # simplemente en consola muestre none y despliegue el error en la tabla
        return None