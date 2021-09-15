#Importaciones y declaraciones  Globales
from codeditor.jolc.jolc.Error import *
import os
import re
import sys

# Tabla de errores que capturara los errores lexicos y sintacticos
tablaerrores = []

'''
▄▄▄▄▄ Analizador Lexico para el Lenguaje de Programacion 'Jolc'▄▄▄▄▄▄▄▄▄▄▄▄▄
█       Autor : Erick Daniel Poron Muñoz                                    █
█       Fecha : 15/08/2021                                                  █
█       Descripcion: Generar el analisis lexico para una entrada de texto   █
█                    los cuales seran asignados a sus respectivos tokens    █
█                    siempre y cuando sean validos en Julia                 █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
'''

'''
    Declaracion de las palabras reservadas en el lenguaje
    se colocan en un diccionario para evitar colocar para cada una
    un estado para el token
'''

palabras_reservadas = {
    # simbolo_encontrado : token_devolver 

    # Palabras que nos serviran para validar datos
    'Array' :    'Array',
    'Int64' :    'Int64',
    'Float64' :  'Float64',
    'Bool' :     'Bool',
    'Char' :     'Char',
    'String' :   'String',
    'struct' :   'struct',
    'nothing' :  'nothing',
    
    # Palabra que definira una variable como constante que no puede ser modificada
    'mutable' : 'mutable',
    
    # Instruccion de fin se sentencia
    'end' : 'end',
    
    # Funciones de cadenas
    'uppercase' : 'uppercase',
    'lowercase' : 'lowercase',
    
    # Funciones matematicas
    'log10' :  'log10',
    'log' :    'log',
    'sin' :    'sin',
    'cos' :    'cos',
    'tan' :    'tan',
    'sqrt' :   'sqrt',
    
    # Funciones de impresion
    'print' :   'print',
    'println' : 'println',

    # Manejo de referencia a ambitos de variable
    'local' :   'local',
    'global' :  'global',
    
    # Funciones
    'function' : 'function',
    
    # Funciones nativas
    'parse' :  'parse',
    'trunc' :  'trunc',
    'float' :  'float',
    'string' : 'string',
    'typeof' : 'typeof',

    # Involucran Arreglos
    'push'  :   'push',
    'pop'   :   'pop',
    'length' :  'length',   # Puede ser un struct o una cadena

    # Sentencias condicionales
    'if' :     'if',
    'elseif' : 'elseif',
    'else' :   'else',

    # Ciclos
    'for' :   'for',
    'in' :    'in',
    'while' : 'while',

    # Sentencias de Transferencia
    'break' :    'break',
    'continue' : 'continue',
    'return' :  'return',

}


'''
    Declaracion de Estados de los Token, seran los signos y
    palabras reservadas declaradas anteriormente
'''

tokens = [
    # Delimitadores
 #   'dolar',
    'terminator',       # ;
    'comma',            # ,
    'point',            # .
    'definir',          # ::
    'twopoint',         # :
    'lparen',           # (
    'rparen',           # )
    'lsqbrack',         # [
    'rsqbrack',         # ]
    'lkey',             # {
    'rkey',             # }

    # Aritmeticos
    'plus',             # +
    'minus',            # -
    'div',              # /
    'mul',              # *
    'mod',              # %
    'exp',              # ^
    
    # Relacionales
    'gte',              # >=
    'lte',              # <=
    'gt',               # >
    'lt',               # <
    'eq',               # ==
    'neq',              # !=

    # Asignacion
    'equal',            # =

    # Logicos
    'and',              # &&
    'or',               # ||
    'no',               # !


    # Valores 
    'valor_cadena',     # ER String
    'valor_caracter',   # ER Char
    'valor_entero',     # ER Int64
    'valor_decimal',    # ER Float64
    'verdadero',        # ER true
    'falso',            # ER false

    # identifier
    'identifier',       # ER Identificador
    
    ] + list(palabras_reservadas.values())

# Definicion de Estados y definicion de su signos

# Delimitadores
t_terminator =      r';'
t_comma =           r','
t_point =           r'\.'
t_definir =         r'::'
t_twopoint =        r':'
t_lparen =          r'\('
t_rparen =          r'\)'
t_lsqbrack =        r'\['
t_rsqbrack =        r'\]'
t_lkey  =           r'\{'
t_rkey  =           r'\}'
# Matematicos
t_plus =           r'\+'
t_minus =          r'-'
t_div =            r'/'
t_mul =            r'\*'
t_mod =            r'%'
t_exp =            r'\^'


# Relacionales
t_gte =            r'>='
t_lte =            r'<='
t_gt =             r'>'
t_lt =             r'<'
t_eq =             r'=='
t_neq =            r'!='

# Logicos
t_and =           r'&&'
t_or =            r'\|\|'
t_no =            r'!'

# Asignacion
t_equal =         r'='


# Caracteres a omitir
t_ignore  =       ' \t'  #(ESPACIO, TAB)



# EXPRESIONES REGULARES

 # Valores para los tipos de datos y tokens importantes a tratar 

def t_verdadero(t):
    r'true'
    t.value = True
    return t

def t_falso(t):
    r'false'
    t.value = False
    return t
    
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value,'identifier')   
    return t

def t_valor_decimal(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_valor_entero(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_valor_cadena(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_valor_caracter(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1] 
    return t


# Expresiones o Simbolos a ignorar

def t_comment(t):
    r'(\#\=(.|\n)*?\=\#)|(\#.*)'
    t.lexer.lineno += t.value.count('\n')
    pass


def t_saltolinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
  
#Ignorar retornos de carro agregados por codemirror
def t_retornocarro(t):
    r'\r+'

# Funcion para extrar la columna en la que se genero el erro
def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1

# Error Lexico
def t_error(t):
    lexycalerror = LexycalError(desc =Description.LEXYCAL_SYMB_INVALID, token=t.value[0],row = t.lineno,col=find_column(input, t))
    tablaerrores.append(lexycalerror)
    t.lexer.skip(1)
   

# Construir analizador lexico
import codeditor.jolc.ply.lex as lexico
lexer = lexico.lex()                               # Utilizar mientras se construye el lexer para ir generando cambios
#lexer = lex.lex(optimize=1,lextab="footab")    # Utilizar al finalizar el analizador lexico para hacerlo mas optimo Solo debe hacer esto cuando su proyecto se haya estabilizado y no necesite realizar ninguna depuración.



'''
▄▄▄▄▄ Analizador Sintactico para el Lenguaje de Programacion 'Jolc'▄▄▄▄▄▄▄▄▄
█       Autor : Erick Daniel Poron Muñoz                                    █
█       Fecha : 17/08/2021                                                  █
█       Descripcion: Generar el analisis sintactico para una entrada de     █
█                    tokens validos en la sintaxis del lenguaje de          █
█                    programacion Julia                                     █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
'''
#from Abstract.Node import Tree
from codeditor.jolc.jolc.Program  import Program as Program
from codeditor.jolc.jolc.Instruction.InstructionList import InstructionList
from codeditor.jolc.jolc.Instruction.Conditional import If,ElseIf
from codeditor.jolc.jolc.Instruction.Assignament import Assignament
from codeditor.jolc.jolc.Instruction.Calling import CallFunction
from codeditor.jolc.jolc.Instruction.Console import ShowConsole
from codeditor.jolc.jolc.Instruction.Definition import Definition
from codeditor.jolc.jolc.Instruction.For import For
from codeditor.jolc.jolc.Instruction.Function import FunctionDecl
from codeditor.jolc.jolc.Instruction.Struct import Struct
from codeditor.jolc.jolc.Instruction.While import While
from codeditor.jolc.jolc.Expression.Accestruct import AccesStruct
from codeditor.jolc.jolc.Expression.Array import Array,AccesArray,Slice,Container,OperationArArray,OperationNativeArray,operatorArray
from codeditor.jolc.jolc.Expression.Evaluacion import EvalType
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Native import Native
from codeditor.jolc.jolc.Expression.Operation import Arithmetic,Boolean,UArithmetic,UBoolean
from codeditor.jolc.jolc.Expression.Parameter  import FormalParam
from codeditor.jolc.jolc.Expression.Primitive import ValBool,ValCaracter,ValFloat,ValInteger,ValNothing,ValString
from codeditor.jolc.jolc.Expression.Transferencia import Return,Break,Continue

disable_warnings = True
###############################################################################
#                                                                             #
#  PRECEDENCIA                                                                #
#                                                                             #
###############################################################################
precedence = (
    ('left',  'comma'),                  # ,          Coleccion de operadores
    ('right', 'definir','equal'),        # :: =       Eval y  Asignacion o Declaracion
    ('left',  'or'),                     # ll         suma logica
    ('left',  'and'),                    # &&         multiplicacion logica
    ('left',  'eq','neq'),               # == !=      evaluador de igualdad
    ('left',  'lt','gt','lte','gte'),    # < <= > >=  evaluador de ponderacion
    ('left',  'plus', 'minus'),          # + -        suma y resta aritmetica
    ('left',  'mul', 'div','mod'),       # * , /, %   multiplicacion y division aritmetica   
    ('right', 'uplus','uminus','neg'),   # + - !      operadores unarios
    ('right', 'exp'),                    # ^          potencia 
    ('left',  'point'),                  # .          operador de acceso
    ('left',  'twopoint','in'),          # :          operadores de iteracion
    ('left',  'lparen', 'rparen'),       # ( )        parentesis
)



###############################################################################
#                                                                             #
#  PRODUCCION INICIAL                                                         #
#                                                                             #
###############################################################################
start = 'jolc'



#   Produccion inicial
def p_jolc(p):
    '''
        jolc    :   statement_list
    '''
    p[0] = Program(instructions=p[1])  


    
###############################################################################
#                                                                             #
#  LISTA DE SENTENCIAS                                                        #
#                                                                             #
#-##############################################################################
#   Produccion que maneja una lista de sentencias
def p_statement_list(p):
    '''
        statement_list : statement terminator 
                       | statement_list statement terminator 
                       | 
    '''
    if len(p) == 3:# La primera sentencia deriva de la raiz
        p[0] = InstructionList(declarations=[p[1]])   
    elif len(p) == 4:#Las demas sentencias derivan recursivamente por lo que se agregan a la inicial    
        p[1].declarations.append(p[2])
        p[0] = p[1]
    else:#No se produjeron sentencias por lo que el cuerpo del programa esta vacio
        p[0] = InstructionList()



###############################################################################
#                                                                             #
#  SENTENCIAS                                                                 #
#                                                                             #
###############################################################################

def p_statement(p):
    '''
    statement : expression 
              | if_statement
    '''
    p[0] = p[1] #Deriva de una sentenciaif o una expression (Las validaciones se realizan en el semantico)



###############################################################################
#                                                                             #
#                           SENTENCIAS CONDICIONALES                          #
#                                                                             #
###############################################################################

#   Sentencia Condicional If
def p_if_elseif_else_statement(p):
    '''
            if_statement :   if  expression  statement_list  elseif_clause end
                         |   if  expression  statement_list  elseif_clause else_clause end
    '''
    if len(p) == 6 :#Deriva una Sentencia if con una lista de elseif
        p[0] = If(condition = p[2],instructions =p[3],alternatives = p[4], row = p.lineno(1),col = find_column(input, p.slice[1]))
    else:#Deriva una Sentencia if con una lista de elseif y las instrucciones del else
        p[0] = If(condition = p[2],instructions =p[3],alternatives =p[4], nomatches_instruction = p[5], row = p.lineno(1),col = find_column(input, p.slice[1]))
    
def   p_if_else_statement(p):
    '''
        if_statement     :   if  expression  statement_list  end
                         |   if  expression  statement_list  else_clause end
    ''' 
    if len(p) == 5:#Deriva una sentencia if sin elseif ni else
        p[0] = If(condition = p[2],instructions =p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))
    else:#Deriva una sentencia if unicamente con sentencia else
        p[0] = If(condition = p[2],instructions =p[3], nomatches_instruction = p[4], row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Casos alternativos de la sentencia If
def p_elseif_clause(p):
    '''
        elseif_clause   :   elseif  expression  statement_list
                        |   elseif_clause elseif  expression  statement_list 
    '''
    if len(p) == 4: # Deriva una sentencia elseif    
        p[0] = [ ElseIf(condition = p[2],instructions = p[3], row = p.lineno(1),col = find_column(input, p.slice[1])) ]
    else:   # Derivan mas sentencias elseif
        p[1].append(ElseIf(condition = p[3],instructions = p[4], row = p.lineno(1),col = find_column(input, p.slice[2])))
        p[0] =  p[1]


#   Caso final de la sentencia if
def p_else_clause(p):# Deriva una Lista de sentencias en caso no se cumpla ninguna condicion 
    ''' 
        else_clause :   else statement_list
    '''
    p[0] = p[2]

###############################################################################
#                                                                             #
#                                FUNCIONES                                    #
#                                                                             #
###############################################################################


def p_function_statement(p):# Deriva una declaracionn de funcion
    '''
        statement :   function identifier lparen   arguments  rparen statement_list end
    '''
    p[0] = FunctionDecl(func_name=p[2],formal_params=p[4],block_func = p[6], row = p.lineno(1),col = find_column(input, p.slice[1]))
    


###############################################################################
#                                                                             #
#                               IMPRESION EN CONSOLA                          #
#                                                                             #
###############################################################################

#   Imprimir sin salto de linea
def p_print_statement(p):# Deriva impresion en consola sin salto de linea
    '''
        statement   :   print lparen arguments  rparen   
    '''
    p[0] = ShowConsole(expression=p[3],nextline=False, row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Imprimir con salto de linea
def p_println_statement(p):# Deriva una impresion en consola con salto de linea
    '''
        statement   :   println lparen arguments  rparen   
    '''
    p[0] = ShowConsole(expression=p[3],nextline=True, row = p.lineno(1),col = find_column(input, p.slice[1]))


###############################################################################
#                                                                             #
#                           SENTENCIAS REPETITIVAS                            #
#                                                                             #
###############################################################################

def p_while_loop(p):  # Deriva un ciclo while
    '''
    statement : while expression  statement_list end
    '''
    p[0] = While(condition=p[2],instructions=p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))
    


def p_for_loop(p):  # Deriva un ciclo for
    '''
    statement   :   for container statement_list end %prec in
    '''
    p[0] = For(iterable=p[2],instructions=p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))


###############################################################################
#                                                                             #
#  STRUCTS                                                                    #
#                                                                             #
###############################################################################

#   Definicion de struct
def p_struct_definition(p): # Deriva de una declaracion de struct
    '''
        statement    :   struct identifier struct_parameters end
                     |   mutable struct identifier struct_parameters end
    '''
    if len(p)== 5:
        p[0] = Struct(identifier= p[2],members=p[3],mutable=False, row = p.lineno(1),col = find_column(input, p.slice[1]))
    else:
        p[0] = Struct(identifier= p[3],members=p[4], row = p.lineno(1),col = find_column(input, p.slice[1]))


###############################################################################
#                                                                             #
#  TIPOS DE DATOS                                                             #
#                                                                             #
###############################################################################

def p_type_data(p): # Tipos de dato validos (Validar en el semantico cuando es ID ya que sera un TDA creado con un struct)
    '''
    type_data : Int64
              | Float64
              | Bool
              | Char
              | String
              | id
    '''
    p[0] = p[1]


###############################################################################
#                                                                             #
#  EXPRESIONES                                                                #
#                                                                             #
###############################################################################

# Deriva un tipo de dato primitivo, un acceso a un arreglo o una operacion a un arreglo
def p_expression(p):
    ''' 
        expression  :   primitive
                    |   array_access
                    |   array_operator
                    |   type_data

    '''
    p[0] = p[1]

###############################################################################
#                                                                             #
#  VALORES PRIMITIVOS                                                         #
#                                                                             #
###############################################################################


def p_value_primitive_entero(p):    # Es un numero entero
    '''
        primitive   :   valor_entero
    '''
    p[0] = ValInteger(value=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_value_primitive_decimal(p):   # Es un numero decimal
    '''
        primitive   :   valor_decimal
    '''
    p[0] = ValFloat(value=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_value_primitive_cadena(p):    # Es una cadena 
    '''
        primitive   :   valor_cadena
    '''
    p[0] =  ValString(value=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_value_primitive_caracter(p):  # Es un Caracter
    '''
        primitive   :   valor_caracter
    '''
    p[0] =  ValCaracter(value=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_value_primitive_boolean(p):   # Es un valor Booleano
    '''
        primitive   :   verdadero
                    |   falso
    '''
    p[0] =  ValBool(value=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))


def p_ValNothing(p):    # Es nada
    '''
        expression  :   nothing 
    '''
    p[0] =  ValNothing(value=None, row = p.lineno(1),col = find_column(input, p.slice[1]))


# Operator array
def p_array_operator_native(p):
    '''
        array_operator : native point expression
    '''
    p[0] = OperationNativeArray(tiponative=p[1],array_access=p[3],row = p.lineno(2),col = find_column(input, p.slice[2]))

def p_array_operator_op(p):
    '''
        array_operator : expression  point oparray
    '''
    p[0] = OperationArArray(array_access=p[1], operator= p[3],row = p.lineno(2),col = find_column(input, p.slice[2]))
      

def p_op_array(p):
    '''
        oparray :   plus expression 
                |   minus expression 
                |   mul expression
                |   div expression
                |   mod expression 
                |   exp expression
    '''
    p[0] = operatorArray(op=p[1],exp=p[2],row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Expresion que deriva de una asignacion/declaracion  
def p_declaration_asignation(p):# id seria para instrucciones que lo requieran, definicion o asig para la tabla de simbolos
    '''
        expression   :   global expression
                     |   local expression 
    '''
    if len(p) == 3 :
        p[0] = Definition(valScope= p[1],expression=p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))
    else:     
        p[0] = p[1]



def p_assignament(p):# Asignar un valor o declarar (ID, Arreglo, Structura)
    '''
        expression : expression equal expression  
    '''
    p[0] = Assignament(left=p[1],right=p[3], row = p.lineno(1),col = find_column(input, p.slice[2]))


def p_definetype(p): # Define el tipo a evaluar en la asignacion, solo los arreglos mantiene el valor
    '''
        expression   :   expression definir type_data 
                     
    '''   
    p[0] =  EvalType(expression=p[1],type_data=p[3], row = p.lineno(2),col = find_column(input, p.slice[2]))




# Expresion deriva en una operacion binaria aritmetica (+,-,*,/,^,%)
def p_binary_arithmetic(p):
     '''
        expression  : expression plus   expression    
                    | expression minus  expression     
                    | expression mul    expression 
                    | expression div    expression 
                    | expression mod    expression 
                    | expression exp    expression
     '''
     p[0] = Arithmetic(left=p[1],op= p[2],right= p[3], row = p.lineno(1),col = find_column(input, p.slice[2]))

# Expresion deriva en una operacion unaria aritmetica (+,-)
def p_unary_arithmetic(p):
    '''
        expression  :   plus   expression   %prec   uplus  
                    |   minus    expression %prec   uminus       
    '''
    p[0] = UArithmetic(op= p[1],val= p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))


#   Expresion deriva en una operacio binaria booleana relacional   (>=,<=,>,<,==,!=) 
#   Aca se encuentra el and y el or ya que todas las expresiones devuelven un valor de verdad
def p_binary_boolean(p):
     '''
        expression  : expression  gte  expression 
                    | expression  lte  expression 
                    | expression  gt   expression 
                    | expression  lt   expression 
                    | expression  eq   expression 
                    | expression  neq  expression 
                    | expression  and  expression 
                    | expression  or   expression 
     '''
     p[0] = Boolean(left=p[1],op=p[2],right=p[3], row = p.lineno(1),col = find_column(input, p.slice[2]))


#   Expression deriva en la operacion unaria booleana (!)
def p_unary_boolean(p):
    '''
        expression  :   no   expression  %prec   neg           
    '''
    p[0] = UBoolean( op=p[1],val=p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))


#   Llama a una funcion 
def p_call_function_struct(p):
    '''
        expression  :   identifier  lparen arguments rparen   
    '''
    p[0] = CallFunction(func_name=p[1],parameters=p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))


#   Arreglo
def p_arrays(p):
    '''
        expression  :   lsqbrack arguments rsqbrack 
                    
    '''
    p[0] = Array(items=p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_array_tipe(p):
    '''
        expression  :   lsqbrack arguments rsqbrack  definir Array lkey type_data rkey 
                    
    '''
    p[0] = Array(items=p[2], type_data_array=p[7], row = p.lineno(1),col = find_column(input, p.slice[1]))




def p_slice_cadena(p):
    '''
        expression : valor_cadena lsqbrack expslice rsqbrack
    '''
    p[0] = ValString(value=p[1],rango=p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))


#   Acceso a un arreglo
def p_array_access(p):
    '''
        array_access  :   identifier  list_index
    '''
    p[0] = AccesArray(identifier=p[1],items=p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))


def p_list_index(p):
    '''
        list_index : lsqbrack argsarray rsqbrack
                   | list_index  lsqbrack argsarray rsqbrack  
    '''
    if len(p) == 4:
        p[0] =   [p[2]]   # Una unico index
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_args_array(p):
    '''
        argsarray : expslice
    '''
    p[0] = p[1]


def p_slice_exp(p):
    '''
        expslice : slice_copy
                 | slice_left
                 | slice_right
                 | slice_all
                 | expression
    '''
    p[0] = p[1]


#   Devuelve una copia
def p_slice(p):
    '''
        slice_copy : twopoint  
    '''
    p[0] = Slice(row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_slice_start(p):
    ''' 
        slice_left : expression twopoint  
    '''
    p[0] = Slice(startslice=p[1],row = p.lineno(1),col = find_column(input, p.slice[2]))

def p_slice_end(p):
    '''
        slice_right : twopoint expression 
    '''
    p[0] = Slice(endslice=p[2],row = p.lineno(1),col = find_column(input, p.slice[1]))


#   Devuelve un trozo start:end
def p_slice_start_end(p):
    '''
        slice_all  : expression twopoint   expression                
    '''
    p[0] = Slice(startslice=p[1],endslice=p[3], row = p.lineno(1),col = find_column(input, p.slice[2]))



#   Sirve para iterar o saber si un valor se encuentra dentro de la otra expression
def p_container(p):
    '''
        container  :   identifier  in  argscontainer 
    '''
    p[0] = Container(item=p[1],container=p[3], row = p.lineno(1),col = find_column(input, p.slice[1]))

def p_argscontainer(p):
    '''
        argscontainer : slice_all
                      | expression
                      
    '''
    p[0] = p[1]

#   Sentencia que interrumpe una sentencia de repeticion
def p_sentence_break(p):
    '''
        expression      :   break
    '''
    p[0] = Break( row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Sentencia que salta una iteracion en una sentencia de repeticion
def p_sentence_continue(p):
    '''
        expression   :   continue
    '''
    p[0] = Continue( row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Sentencia que devuelve un valor 
def p_sentence_return(p):
    '''
        expression  :   return  expression   
    '''
    p[0] = Return(p[2], row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Expression deriva en una expresion entre parentesis
def p_paren_operation(p):
    '''
        expression  :   lparen  expression  rparen
    '''
    p[0] = p[2]

#   Produccion para acceder a un valor mediante un punto u operar
def p_acces_point(p):
    '''
        expression  :   id listpoint
    '''
    p[0] = AccesStruct(identifier=p[1],item=p[2], row = 0,col = 0)

#  Acceso a Structs de structs

def p_listpoint(p):
    '''
        listpoint  : point identifier 
                   | listpoint  point identifier  
    '''
    if len(p) == 3:
        p[0] =   [p[2]]   # Una unico index
    else:
        p[1].append(p[3])
        p[0] = p[1]


###############################################################################
#                                                                             #
#  FUNCIONES NATIVAS                                                          #
#                                                                             #
###############################################################################

def p_function_native(p):# Deriva una funcion nativa 
    '''
        expression :   native  lparen arguments rparen                   
    '''
    p[0] = Native(typefunction=p[1], parameters=p[3], row = p.lineno(1),col = find_column(input, p.slice[2]))
 
        
    

def p_native(p):# Deriva que tipo de operacion nativa se va a ejecutar
    '''
        native     :   sin
                   |   cos
                   |   tan
                   |   sqrt
                   |   log10 
                   |   uppercase
                   |   lowercase
                   |   trunc
                   |   float
                   |   string
                   |   typeof
                   |   length
                   |   log
                   |   parse
                   |   push no
                   |   pop  no
    '''
    if(len(p) == 3):
        p[0] = p[1] + 'no'
    else:
        p[0] = p[1]


 
###############################################################################
#                                                                             #
#                   PRODUCCIONES GLOBALES UTILES                              #
#                                                                             #
###############################################################################


#   Produccion que almacena el identificador 
def p_id(p):
    '''
        id  :   identifier
    '''
    p[0] =  Identifier(identifier=p[1], row = p.lineno(1),col = find_column(input, p.slice[1]))

#   Lista de expresiones separadas por comma


    
def p_arguments(p):
    '''
        arguments   :   expression 
                    |   arguments comma expression  
                    |   
    '''
    if len(p) == 2:
        p[0] =   FormalParam(var_node=[p[1]])    # Una unica instruccion
    elif len(p) == 4:
        p[1].var_node.append(p[3])
        p[0] = p[1]
    else:
        p[0] =  FormalParam()

#   Produccion para generar los miembros de un struct separados por ;
def p_struct_parameters(p):
    '''
        struct_parameters    :  expression terminator
                             |  struct_parameters expression terminator 
                             |  
    '''
    if len(p) == 3:
        p[0] =  FormalParam(var_node=[p[1]])   # Una unica instruccion
    elif len(p) == 4:
        p[1].var_node.append(p[2])
        p[0] = p[1]
    else:
        p[0] = FormalParam()



###############################################################################
#                                                                             #
#  PRODUCCION ERROR (MODO PANICO)                                             #
#                                                                             #
###############################################################################
def p_error(p):

    if not p:
        #print("End of File!")
        return
    
    esintaxis= SintaxError(desc=Description.SINTAX_ERROR , token=str(p.value),row=p.lineno,col=find_column(input, p))
    tablaerrores.append(esintaxis)

    # Consume todos los tokens hasta encontrar un fin de sentencia y regresa a la produccion inicial
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'terminator': 
            break
    parser.errok()
    return tok



###############################################################################
#                                                                             #
#  GENERAR PARSER                                                             #
#                                                                             #
###############################################################################
import   codeditor.jolc.ply.yacc as sintactico  
parser = sintactico.yacc()

def get_parser(text_input):
    global tablaerrores
    global lexer
    global parser
    global input
    input = text_input
    lexer  = lexico.lex()
    parser = sintactico.yacc(errorlog=sintactico.NullLogger()) if disable_warnings else sintactico.yacc()

    programa = parser.parse(text_input)    #El ast devuelve una instancia de Programa
    if(programa is not None):
        programa.errores = tablaerrores
    else: 
        print("Ocurrio un error Irrecuperable en el anilisis, devuelve None")

    return programa

def get_Errores():
    return tablaerrores