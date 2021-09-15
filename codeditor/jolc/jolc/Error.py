from enum import Enum
from datetime import datetime

class Description(Enum):
    # Errores Lexicos
    LEXYCAL_SYMB_INVALID    = "Simbolo no reconocido"
    
    #Errores Sintacticos
    SINTAX_ERROR           = "Error de sintaxis"

    #Errores Semanticos
    SEMANTIC_ID_DUPLICATE = "La variable a declarar ya existe en el ambito actual"
    SEMANTIC_ID_404	= "La variable no esta declarada"
    SEMANTIC_ARRAY_DUPLICATE = "El arreglo a declarar ya existe en el ambito actual"
    SEMANTIC_STRUCT_DUPLICATE = "El tda a declarar ya existe en el ambito actual"
    SEMANTIC_FUNCTION_DUPLICATE = "La Funcion a declarar ya existe en el ambito actual"
    SEMANTIC_TRANSFERENCE_LOCATION = "La sentencia de Transferencia No se Encuentra en un ciclo"
    SEMANTIC_UNARY_AEVAL = "No se puede evaluar la expresion Unaria Arithmetica"
    SEMANTIC_UNARY_BELVA = "No se puede evaluar la expresion Unaria Booleana"
    SEMANTIC_AEVAL = "No se puede evaluar la expresion Aritmetica"
    SEMANTIC_BELVA = "No se puede evaluar la expresion Booleana"
    SEMANTIC_OPERATOR_AINVALID   = "Operador Aritmetico Invalido"
    SEMANTIC_OPERATOR_BINVALID  = "Operador Booleano Invalido"
    SEMANTIC_OPERADOR_RINVALID = "Operador Relacional Invalido"
    SEMANTIC_EVAL_TAUNARY = "Solo se pueden evaluar tipos (Int64 Float64)"
    SEMANTIC_EVAL_TBUNARY = "La expresion no retorna un tipo Bool"
    SEMANTIC_EVAL_ATIPO = "Tipo Invalido dentro de la operacion Aritmetica"
    SEMANTIC_EVAL_BTIPO = "Tipo Invalido dentro de la operacion Booleana"
    SEMANTIC_EVAL_NATIVE = "Error en la evaluacion de la Nativa"
    SEMANTIC_ASSIG_NOTYPE = "El valor de la expression no coincide con el tipo a asignar"
    SEMANTIC_ASSIG_ARRAY = "No se puede Ingresar un valor de tipo invalido en el arreglo"
    SEMANTIC_NOBOOL	= "La expresion no retorna un valor Booleano"
    SEMANTIC_DECL_STRUCT = "Solo puedes declarar struct en el ambito global"
    SEMANTIC_STRUCT_TMEM = "El struct declara Tipo Invalido"
    SEMANTIC_STRUCT_RDECL = "El struct ya ha sido declarado"
    SEMANTIC_INVALID_VAR = "La Expresion que desea agregar no es un valor con propiedad asignable"
    SEMANTIC_GLOBAL_GLOBAL = "No se puede usar global en el ambito Global"
    SEMANTIC_GLOBAL_RDCL = "Ya se a declarado esta referencia a la variable global"
    SEMANTIC_NODECL_GLOBAL = "Solo puedes declarar el puntero sin asignar"
    SEMANTIC_NOCALLING	= "La llamada no representa ninguna funcion o tda"
    SEMANTIC_LEN_PARAM = "Faltan parametros obligatorios"
    SEMANTIC_PARAM_NO = "El parametro no representa un simbolo formal"
    SEMANTIC_NO_DI_ARRAY = "El arreglo al que accede, no esta declarado aun o los parametros no coinciden"
    SEMANTIC_NOTYPE_STRUCT= "El valor que desea asignar no coincide con el miembro del struct"
    SEMANTIC_STRUCT_INMUTABLE	= "El struct al que desea asignar es Inmutable"
    SEMANTIC_STRUCT_NOINSTANACE = "La variable no es una instancia de struct"
    SEMANTIC_REF_NOGLOBAL = "La variable que desea referenciar no existe en el ambito global"
    SEMANTIC_LENG_ARRAY = "Uno de los paramtros no coincide con la longitd del arreglo"
    SEMANTIC_ARRAY_404 = "El arreglo que busca aun no ha sido declarado"
    SEMANTIC_VALORNOACCES = "No representa un valor accesible dentro del arreglo"
    SEMANTIC_NOITERABLE = "El valor al que desea asignar no es un Arreglo"
    SEMANTIC_INDEX_NO_INT = "Se necesita un indice de tipo Int64"
    SEMANTIC_TYPE_ARREGLO = "El arreglo tipado no puede recibir otro valor que no es de su tipo"
    SEMANTIC_NOT404_PARAMETER = "No se encontro el struct que se desea referenciar"
    SEMANTIC_TDA_NO_COINCIDE = "La variable que referencio no coincide con el tipo de struct"
    SEMANTIC_NO_MEMBER  = "El valor que busca no es un miembro del tipo de dato"
    SEMANTIC_PARAMETER_NOSTRUCT = "Debe referenciar una variable struct como parametro"
    SEMANTIC_NOTYPE_MEMBER_ASIGN = "El valor del miembro no es corracto, debe asignar el valor adecuado"
    WARNIGN_PARAMETRO_NOAGREGADO = "Warning: Parametro no agregado "
    SEMANTIC_FOR_NONVALIDAD_EXP = "La expression de argumento del ciclo es invalida"
    SEMANTIC_NON_ITERABLE = "La expression no representa un valor iterable"
    SEMANTIC_NON_RANGE = "El rango debe expresar un numero de inicio y uno de final"
    SEMANTIC_NON_LENGHT_CADENA = "El rango excede en la longitud de la cadena"
    
    def __str__(self):
        return self.value

class Error():
    def __init__(self, desc = None, token = None, row =None, col=None, tiempo_ocurrencia=datetime.now()):
        self.desc = desc
        self.token = token
        self.row       = row
        self.col     = col
        self.tiempo_ocurrencia = tiempo_ocurrencia
    def __str__(self):
        return f'{self.__class__.__name__}: {self.desc} with:{self.token}  row:{self.row} col:{self.col}  on:{self.tiempo_ocurrencia}.'
    __repr__ = __str__

class LexycalError(Error):
    pass


class SintaxError(Error):
    pass


class SemanticError(Error):
    pass
