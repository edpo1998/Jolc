'''
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  Clase Global    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█       Autor : Erick Daniel Poron Muñoz                                                      █
█       Fecha : 22/08/2021                                                                    █
█       Descripcion: La presente clase pretende alojar el ambiente global de toda la          █
█                    ejecucion, ya que la interpretacion se realiza en una sola pasada        █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
'''
from codeditor.jolc.jolc.Error import Description, SemanticError
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Table.ScopedTable import *
from codeditor.jolc.jolc.Table.Symbol  import *
import pprint

class Program(Tree):
   
    def __init__(self,instructions = None, errores = []):
        # Inicializamos una tabla de simbolos global
        self.global_scope = GlobalScope(
            scope_name  = 'global',                # Iniciamos en el ambito global
            scope_level = 1 ,                      # El nivel de anidacion sera el nivel 1 ya que 0 es para modulos en caso de implementacion
            enclosing_scope= None,                 # No le precede ningun ambito (None)
        )
        self.instructions = instructions           # Instrucciones del programa
        self.errores = errores                     # Errores obtenidos
        self.ambitos = {}                          # Referencia a Funciones
        self.tda = {}                              # Tipos de datos definidos por struct
        self.output = ''                           # Salida en consola
        self.lastScope = self.global_scope         # Ultimo ambito declarado      
        self.tablasimbolos = None                  # Sobre esta variable construiremos el reporte de la tabla de simbolos            


    def __str__(self):
        return f'<Program instrucciones: {self.instructions} >'

    def updateLast(self,scope):
        self.lastScope = scope

    # Agrega un error semantico 
    def addError(self,desc,token,row,col):
        self.errores.append(SemanticError(desc=desc,token=token,row=row,col=col))

    # Agrega un nuevo ambito de funcion de nivel 2
    # Es para tener la certeza, ya que los siguientes ambitos anidados 
    # no poseeran las mismas caracteristicas
    def addScope(self,func): # El parametro recibido es un simbolo
        funcion = self.ambitos.get(func.func_name)
        if funcion is not None: # Error de redeclaracion
            self.errores.append(SemanticError(desc=Description.SEMANTIC_FUNCTION_DUPLICATE,token=func.func_name,row=func.row,col=func.col))
        else:
            self.ambitos[func.func_name] = func     # Tomar en cuenta que nada mas es el simbolo de la funcion como tal

    # Obtiene el simbolo de la funcion para su ejecucion
    def getScope(self,name):
        funcion = self.ambitos.get(name)
        return funcion

   # Obtiene una lista de miembros con el tipo que deberian contener
   # No es un simbolo en si, solo es la estructura para validar la creacion del 
   # simbolo que se creara de su instancia en la llamada a una funcion
    def getTDA(self,name):
        structure = self.tda.get(name)
        return structure

    # Agrega un mensaje en consola
    def addConsole(self,msg):
        self.output = self.output + msg

    # Muestra los errores generados en las 3 fases del analisis del front-end
    def show_Errors(self):
        console = pprint.PrettyPrinter()
        for error in self.errores:
            ec = error
            console.pprint(ec)


    def BuildReport(self):
        tablasimbolos = []
        scopes = self.ambitos
        self.global_scope.showSymbols(tablasimbolos)
        for key in scopes:
            funcion = scopes[key]
            tablasimbolos.append([f'{funcion.scope_level}'f'{funcion.func_name}','Function',f'global',f'{funcion.row}',f'{funcion.col}'])
            if(funcion.ref is not None):
                funcion.ref.showSymbols(tablasimbolos)
        self.tablasimbolos = tablasimbolos