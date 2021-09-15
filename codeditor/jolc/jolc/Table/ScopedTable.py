'''
▄▄▄▄▄▄▄▄▄   Tabla de ambitos anidados para el Lenguaje de Programacion 'Jolc'    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█       Autor : Erick Daniel Poron Muñoz                                                      █
█       Fecha : 22/08/2021                                                                    █
█       Descripcion: Arbol de ambitos anidados , en el cual cada ambito poseera sus           █
█                    propia declaracion de simbolos                                           █
█                                                                                             █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
'''

from codeditor.jolc.jolc.Table.Symbol import  Var

class ScopedTable:

    def __init__(self, scope_name=None,scope_level=None, enclosing_scope=None):
        self.scope_name = scope_name                #  Nombre del Scope
        self.scope_level = scope_level              #  Nivel de anidamiento   
        self.enclosing_scope = enclosing_scope      #  Si le Precede de un ambito, almacena la referencia
        self.symbols = {}                           #  Simbolos de ambito local (Al iniciar la tabla de nivel 0 sera global a todo el programa)

    # Definicion del metodo str
    def __str__(self):
        titulo = 'AMBITO - TABLA DE SIMBOLOS'
        lines = ['\n', titulo, '=' * len(titulo)]
        for header_name , header_value in (
            ('Ambito:', self.scope_name),
            ('Anidamiento:', self.scope_level),
            ('Superior:',self.enclosing_scope.scope_name if self.enclosing_scope else None )
        ):  lines.append(f'{header_name:<15}: {header_value}')
        body = '------------ Simbolos ---------------'
        lines.extend([body, '-' * len(body)])
        lines.extend(
            f'{key:>7}: {value}'
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    __repr__ = __str__


    # Mostrar Simbolos
    def showSymbols(self,arr):
        tabla = self.symbols
        for key in tabla: 
            if(isinstance(tabla[key],Var)):
                if(isinstance(tabla[key].value ,list)):
                    arr.append([f'{tabla[key].name}','Array',f'{self.scope_name}',f'{tabla[key].row}',f'{tabla[key].col}'])
                elif(isinstance(tabla[key].value ,dict)):
                    arr.append([f'{tabla[key].name}','Struct',f'{self.scope_name}',f'{tabla[key].row}',f'{tabla[key].col}'])
                else:
                    arr.append([f'{tabla[key].name}','Var',f'{self.scope_name}',f'{tabla[key].row}',f'{tabla[key].col}'])
            
     # Para debbugin y  para poder observar desarrollo de la tabla   
    def showAction(self,msg):
        print(msg)

    # Inserta un nuevo simbolo , la validacion se realiza en el analisis semantico
    def insert(self,sym):
        #self.showAction(f'Insert: {sym.name} Scope: {self.scope_name}')
        sym.scope_level = self.scope_level 
        self.symbols[sym.name] = sym

    # Redeclarar el simbolo para tener certeza del cambio, en el caso del manejo de global 
    def changeSymbol(self,sym):
        simbolo = self.symbols.get(sym.name)
        if simbolo is not None:
            self.symbols[sym.name] = sym

    # Busca por defecto en todos los ambitos, es posible habilitar la opcion de buscar unicamente en el ambito actual
    def lookup(self, name, current_scope_only = False):
        # self.showAction(f'Lookup: {name} (Scope: {self.scope_name} enclosing: {self.enclosing_scope.scope_name if self.enclosing_scope is not None else "Ninguno"})')
        # Obtiene el simbolo en el ambito en el que se encuentra
        symbol = self.symbols.get(name)
        
        if symbol is not None:
            #self.showAction(f'Lookup: {symbol.value} (Scope: {self.scope_name})')
            return symbol
        
        # Pivote para no extender la busqueda a los ambitos adjuntos superiores  hasta llegar al global
        if current_scope_only:
            return None
        
        # Obtiene el ambito adjunto superior de manera recursiva hasta encontrar el simbolo y llegar al nivel 1
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

    # Esta funcion busca en un ambito determinado
    # Define ser para el global porque lo usaremos para ese efecto
    # pero puede buscar en cualquier ambito pasado como argumento
    def lookupGlobal(self, name, scope_global):
        simbolo = scope_global.lookup(name, current_scope_only = True)
        return simbolo

# Ambito General
class GlobalScope(ScopedTable):
    def __init__(self, scope_name, scope_level, enclosing_scope):
        super().__init__(scope_name, scope_level, enclosing_scope=enclosing_scope)
        self.tdas = {}  # Servira para almacenar los tipos de datos definidos con structs

# Ambito de Funcion, las funciones de nivel 2 tienen las propiedades del global, sin embargo no se evaluaron funciones anidadas en el proyecto
class FunctionScope(ScopedTable):
    def __init__(self, scope_name, scope_level, enclosing_scope):
        super().__init__(scope_name, scope_level, enclosing_scope=enclosing_scope)
        self.reference = []  # Referencia a valores Globales

# Ambito para las sentencias repetitivas
class CicloWhile(ScopedTable):
    def __init__(self, scope_name, scope_level, enclosing_scope):
        super().__init__(scope_name, scope_level, enclosing_scope=enclosing_scope)
        self.reference = []  # Referencia a valores Globales


class CicloFor(ScopedTable):
    def __init__(self, scope_name, scope_level, enclosing_scope):
        super().__init__(scope_name, scope_level, enclosing_scope=enclosing_scope)
        self.reference = []  # Referencia a valores Globales



        