from codeditor.jolc.jolc.Table.Symbol import Var #, Struct #,Function
from codeditor.jolc.jolc.Abstract.Node import Tree
from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Table.ScopedTable import FunctionScope 
from codeditor.jolc.jolc.Expression.Identifier import Identifier
from codeditor.jolc.jolc.Expression.Evaluacion import EvalType

class CallFunction(Tree):
    def __init__(self,func_name=None,parameters=None, row=None,col=None):
        super().__init__(row=row, col=col) 
        self.func_name   = func_name     # Funcion a llamar 
        self.parameters  = parameters    # Lista de parametros a imprimir
        # Referencia a la declaracion del simbolo para la pila de llamadas
        # self.func_symbol =None    #Comente esta linea debido a que solo nos servira si
        # la interpretacion la hacemos por medio de una pila y registros de activacion

    def __str__(self):
        return f'<CallFunction id:{self.func_name} parameters:{self.parameters} >'

    def execute(self, tree, table):
        # Simbolo que contiene la Funcion
        callfunc = tree.getScope(self.func_name)    # La funcion ya debio ser declarada por lo tanto devuelvo la instancia de FunctionDecl
        # Diccionario que contiene la estructura segun el tipo que se declaro
        createstruct = tree.getTDA(self.func_name)  # El tipo de dato ya debio ser declarado
        valretorn = None   # Obtiene el valor de retorno en caso de ser una funcion 
        if(callfunc is not None):  # El simbolo devuelto es una funcion
            if(len(callfunc.formal_params.var_node)==len(self.parameters.var_node)):
                #func_symbol = Function(self.func_name) # Creamos nuevo simbolo para la funcion
                #Nueva tabla de anidacion
                function_scope = FunctionScope(
                    scope_name          = self.func_name,                       # Nombre del ambito
                    scope_level         = tree.global_scope.scope_level + 1,    # Nivel de Anidacion sera el siguiente de su predecesor
                    enclosing_scope     = tree.global_scope,                    # Referencia al ambito superior en el que anida
                )
                
                 #Insertamos primero los parametros formales 
                if(len(callfunc.formal_params.var_node) > 0 ):
                    # Podemos usar zip ya que la longitud es la misma
                                                    # Parametros formales , valores pasados como argumentro
                    for formalparam , param in zip( callfunc.formal_params.var_node , self.parameters.var_node):   # FunctionDecl.FormalParam.var_node
                        # La variable no recibe un tipo definido (puede ser variable o arreglo)
                        if isinstance( formalparam , Identifier ):
                            param_name = formalparam.identifier
                            param_val  = param.execute(tree,table)
                            if(not(isinstance(param_val,list))):
                                variablesimbolo = Var(name=param_name,typedata=None,row=self.row,col=self.col,value=param_val)
                                function_scope.insert(variablesimbolo)
                            else:
                                referencia_array = param.getSymb(tree, table)
                                #print(referencia_array.value)
                                variablesimbolo =Var(name=param_name,typedata=None,row=self.row,col=self.col,value=referencia_array.value)
                                function_scope.insert(variablesimbolo)
                        
                        #func_symbol.formal_parameters[param_name] = (variablesimbolo)
                        # La variable recibe un tipo definido por el usuario
                        # Este solo sera validado en la llamada, en el cuerpo puede cambiar
                        elif isinstance( formalparam ,EvalType ):
                            '''
                                expression::type_data
                                Casos:
                                    identificador :: identificador
                                    identificador :: TipoDato (Int6a,Float64,etc..)
                            '''
                            if isinstance(formalparam.expression ,Identifier): # Esto para evitar conflictos ya que lo usamos para otras cosas
                                if(isinstance(formalparam.type_data,Identifier)):
                                    if(isinstance(param,Identifier)):
                                        param_name = formalparam.expression.identifier
                                        param_type = formalparam.type_data.identifier
                                        referencia = formalparam.getStruct(param.identifier,param_type,tree,table)
                                        if(referencia is not None):
                                            variablesimbolo =  Var(name=param_name,typedata=param_type,row=self.row,col=self.col,value=referencia.value,mutabilidad=referencia.mutabilidad)
                                            function_scope.insert(variablesimbolo)
                                        else:
                                            tree.addError(Description.WARNIGN_PARAMETRO_NOAGREGADO,param.identifier,self.row,self.col) 
                                    else:
                                        tree.addError(Description.SEMANTIC_PARAMETER_NOSTRUCT,formalparam.expression.identifier,self.row,self.col)
                                else:
                                     param_name = formalparam.expression.identifier
                                     param_type = formalparam.type_data
                                     result = param.execute(tree,table)
                                     variablesimbolo =  Var(name=param_name,typedata=param_type,row=self.row,col=self.col,value=result)
                                     function_scope.insert(variablesimbolo)
                            else:
                                tree.addError(Description.SEMANTIC_PARAM_NO,self.func_name,self.row,self.col)
                        else:
                            tree.addError(Description.SEMANTIC_PARAM_NO,self.func_name,self.row,self.col)
                callfunc.ref = function_scope;  # Actualizamos la referencia para generar la tabla de simbolos 
                valretorn = callfunc.execute(tree, function_scope)         # INTERPRETAR EL NODO FUNCION
           
            else:
                tree.addError(Description.SEMANTIC_LEN_PARAM,self.func_name,self.row,self.col)

        elif(createstruct is not None):  # Crear un nuevo struct
            #Ya obtuve los parametros del struct
            miembrosconvalor = {} #Contendra el nombre del miembro y su valor
            pivoteparametros = self.parameters.var_node[:]
            if((len(createstruct) - 1)==len(self.parameters.var_node)): # Restar la propiedad mutable
                for tipo in createstruct: 
                    if(tipo != 'mutable'):  # Omitir el parametro de mutabilidad
                        valor = pivoteparametros.pop(0) 
                        valor_asign = valor.execute(tree,table) # Extraemos el valor
                        if(createstruct[tipo] is not None):
                            if(isinstance(valor_asign,createstruct[tipo])):
                                miembrosconvalor[tipo] = valor_asign
                            else:
                                tree.addError(Description.SEMANTIC_NOTYPE_STRUCT,self.func_name,self.row,self.col)
                        else:
                            miembrosconvalor[tipo] = valor_asign
                return{
                    'Tipo': self.func_name,
                    'mutable': createstruct['mutable'],
                    'miembros': miembrosconvalor,
                }
                #print(miembrosconvalor)
                #print(len(self.parameters.var_node))
            else:
                tree.addError(Description.SEMANTIC_LEN_PARAM,self.func_name,self.row,self.col)
        else:
            tree.addError(Description.SEMANTIC_NOCALLING,self.func_name,self.row,self.col)
            
        return valretorn

        

        