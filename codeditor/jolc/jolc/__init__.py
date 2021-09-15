from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Expression.Transferencia import Break, Continue, Return
from codeditor.jolc.jolc.Instruction.Function import FunctionDecl
import codeditor.jolc.jolc.Analyzer.constructor as constructor

import pprint
import sys


from codeditor.jolc.jolc.Table.ScopedTable import *
from codeditor.jolc.jolc.Table.Symbol import *

sys.setrecursionlimit(8000)     # Cambiamos los limites de recursion de python

def execute( source,show_ast: bool=False, show_Output: bool = False,show_scope: bool=False, show_errors: bool=False, disable_warnings:bool=False ):
    # Desactiva los Warnigs del analizador
    constructor.disable_warnings = disable_warnings
    try:
        # Construimos el ast, a traves del analisis lexico y sintactico
        programa = constructor.get_parser(source)           
       
       
        if(programa is not None):
            # Imprime la derivacion del arbol ast en consola
            if show_ast:
                print("\n\n" + '=' * 80, ' == Syntax tree ==')
                pp = pprint.PrettyPrinter()
                pp.pprint(str(programa))
       
            # Ejecucion de manera secuencial e imperativa el programa y realiza el analisis semantico
            for instruction in programa.instructions.declarations:
                if isinstance(instruction, FunctionDecl):
                    programa.addScope(instruction)          #Agrega los simbolos de las funciones
                elif isinstance(instruction,Return) or isinstance(instruction,Continue) or isinstance(instruction,Break):
                    programa.addError(Description.SEMANTIC_TRANSFERENCE_LOCATION,instruction.__class__.__name__,instruction.row,instruction.col)
                else:
                    instruction.execute(programa,programa.global_scope) 

            # Salida en Consola
            if show_Output:
                print(programa.output)

            # Mostrar Ambitos en pantalla
            if show_scope:
                print("--------AMBITOS DE ANIDAMIENTOS--------")
                pp = pprint.PrettyPrinter()
                pp.pprint(str(programa.ambitos))

            # Mostrar errores lexicos, lexicos y semanticos en pantalla
            if show_errors:
                programa.show_Errors()

            # Construccion de la tabla de simbolos
            programa.BuildReport();

        # Devolver el programa
        return programa
               
    except Exception as e:
        print(e.__class__.__name__ + ': ' + str(e), file=sys.stderr)
        if not disable_warnings:
            raise e
    

