import textwrap
from codeditor.jolc.jolc.Expression.Identifier import Identifier

'''
    Metodo para reconocer la instancia del ast que vamos a recorrer
    y asi proceder a trabajar y leer sus atributos.
'''

class Walker:

    def visit(self,node):
        method_name = 'visit_' + type(node).__name__             # visit_nombredelaclaseAST 
        #  getattr se usa para obtener el valor del atributo de un objeto
        #  y si no se encuentra ningún atributo de ese objeto, se devuelve el valor predeterminado.
        visitor = getattr(self, method_name, self.generic_visit) 
        # visitor sera el metodo de la instancia de lo contrario retornar el metodo generico
        return visitor(node)

    def generic_visit(self, node):
        pass#raise Exception('No visit_{} method'.format(type(node).__name__))


class ASTVisualizer(Walker):
    
    def __init__(self,tree):
        self.tree = tree        # AST
        self.contador = 1       # Contador de Nodos del ast
        self.contenido   = []   # Contenido dot del ast

    # Metodo que construye el ast 
    def GenereteAst(self):
        
        encabezado = [textwrap.dedent(
        """\
        digraph Tree {
            node [shape=box3d, fontsize=12, fontname="Courier", height=.1,style=filled, fillcolor=darkseagreen2];
            ranksep=.3;
            edge [arrowsize=.5]
        """
        )] 
        footer = ['}']
        if self.tree is not None:
            sintactree = self.tree
            self.visit(sintactree) 
        return ''.join(encabezado + self.contenido + footer)


    def visit_Program(self, node):
        #  Creamos el nodo con la Informacion
        nodegraph = '  node{} [label=<<B>JOLC</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        # Almacenamos una referencia al numero para que no
        # se pierda despues de recorrer las demas derivaciones
        node._num = self.contador
        self.contador = self.contador + 1
        # Recorremos y creamos el subarbol
        self.visit(node.instructions)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.instructions._num)
        self.contenido.append(nodegraph)


    '''
        ###############################################################################
        #                                                                             # 
        #                               INSTRUCCIONES                                 # 
        #                                                                             #
        ###############################################################################
    '''

    
    def visit_Assignament(self,node):
        nodegraph = '  node{} [label=<<B>Assignament </B> : =>]\n'.format( self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar left
        self.visit(node.left)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.left._num)
        self.contenido.append(nodegraph)
        
        # Generar right
        self.visit(node.right)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.right._num)
        self.contenido.append(nodegraph)
        
    def visit_CallFunction(self,node):
        nodegraph = '  node{} [label=<<B>CallFunction</B> : {} >]\n'.format(self.contador, node.func_name)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar Parametros
        self.visit(node.parameters)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.parameters._num)
        self.contenido.append(nodegraph)

    def visit_If(self,node):
        nodegraph = '  node{} [label=<<B>If</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  condition
        self.visit(node.condition)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.condition._num)
        self.contenido.append(nodegraph)

        # Recorremos y creamos el subarbol
        if node.instructions is not None:
            self.visit(node.instructions)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.instructions._num)
            self.contenido.append(nodegraph)

        # Generar  alternatives
        if node.alternatives is not None:
            for alternative in node.alternatives:
                self.visit(alternative)
                nodegraph = '  node{} -> node{}\n'.format(node._num, alternative._num)
                self.contenido.append(nodegraph)

        # Generamos nomatches_instruction
        if node.nomatches_instruction is not None:
            self.visit(node.nomatches_instruction)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.nomatches_instruction._num)
            self.contenido.append(nodegraph)

    def visit_ElseIf(self, node):
        nodegraph = '  node{} [label=<<B>ElseIf</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Condicion
        self.visit(node.condition)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.condition._num)
        self.contenido.append(nodegraph)

        # Instrucciones
        if node.instructions is not None:
            self.visit(node.instructions)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.instructions._num)
            self.contenido.append(nodegraph)
    

    
    


    def visit_ShowConsole(self,node):
        nodegraph = '  node{} [label=<<B>ShowConsole</B> tipo: {}>]\n'.format(self.contador,'println' if node.nextline else 'print')
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar Parametros
        if node.expression is not None:
            self.visit(node.expression)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.expression._num)
            self.contenido.append(nodegraph)

    def visit_Definition(self,node):
        nodegraph = '  node{} [label=<<B>Scope </B> : {}>]\n'.format( self.contador, node.valScope)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1
      
        # Generar expression
        self.visit(node.expression)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.expression._num)
        self.contenido.append(nodegraph)


    def visit_For(self,node):
        nodegraph = '  node{} [label=<<B>For</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  iterable
        self.visit(node.iterable)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.iterable._num)
        self.contenido.append(nodegraph)

        # Generar  instructions
        self.visit(node.instructions)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.instructions._num)
        self.contenido.append(nodegraph)


    def visit_FunctionDecl(self,node):
        nodegraph = '  node{} [label= <<B>FunctionDecl</B> : {}>]\n'.format( self.contador , node.func_name )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1
        
        # Parametros
        self.visit(node.formal_params)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.formal_params._num)
        self.contenido.append(nodegraph)

        # Instrucciones
        self.visit(node.block_func)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.block_func._num)
        self.contenido.append(nodegraph)


    def visit_InstructionList(self, node):
        nodegraph =  '  node{} [label=<<B>InstructionList</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador + 1
        
        # Generamos todos los nodos 
        # ademas guardamos su numero de nodo en el mismo
        for declaration in node.declarations:
            self.visit(declaration)

        # Teniendo todo disponemos a enlazar 
        for declaration_node in node.declarations:
            nodegraph = '  node{} -> node{}\n'.format(node._num, declaration_node._num)
            self.contenido.append(nodegraph)


    def visit_Struct(self,node):
        nodegraph = '  node{} [label=<<B>Struct</B> : {} >]\n'.format( self.contador, node.identifier)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        if(node.mutable):
            nodegraph = '  node{} [label=<<B>mutable</B>>]\n'.format( self.contador)
            self.contenido.append(nodegraph)
            nodegraph = '  node{} -> node{}\n'.format(node._num, self.contador)
            self.contenido.append(nodegraph)
            self.contador = self.contador + 1

        # Generar Parametros
        self.visit(node.members)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.members._num)
        self.contenido.append(nodegraph)



    def visit_While(self,node):
        nodegraph = '  node{} [label=<<B>While</B>>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  condition
        self.visit(node.condition)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.condition._num)
        self.contenido.append(nodegraph)

        # Generar  instructions
        self.visit(node.instructions)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.instructions._num)
        self.contenido.append(nodegraph)
    



    '''
        ###############################################################################
        #                                                                             # 
        #                               EXPRESIONES                                   # 
        #                                                                             #
        ###############################################################################
    '''


    # ACCESS STRUCT
    def visit_AccesStruct(self,node):
        nodegraph = '  node{} [label=<<B>AccessStruct</B> : {} >]\n'.format(self.contador, node.identifier.identifier  )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar Parametros item
        for index in node.item:
            nodegraph = '  node{} [label=<<B>Item </B> : {} >]\n'.format(self.contador, index  )
            self.contenido.append(nodegraph)
            nodegraph = '  node{} -> node{}\n'.format(node._num, self.contador)
            self.contenido.append(nodegraph)
            self.contador = self.contador +1


    # ARRAY
    def visit_Array(self,node):
        nodegraph = '  node{} [label=<<B>Array</B> tipo: {} >]\n'.format( self.contador, node.type_data_array)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  items
        self.visit(node.items)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.items._num)
        self.contenido.append(nodegraph)

    def visit_AccesArray(self,node):
        # Nodo Raiz
        nodegraph = '  node{} [label=<<B>AccessArray</B> : {} >]\n'.format(self.contador, node.identifier)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  items access
        for index in node.items:
            self.visit(index)
            nodegraph = '  node{} -> node{}\n'.format(node._num, index._num)
            self.contenido.append(nodegraph)

    def visit_Slice(self,node):
        nodegraph = '  node{} [label=<<B>Slice</B> : : >]\n'.format( self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar  startslice
        if(node.startslice is not None):
            self.visit(node.startslice)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.startslice._num)
            self.contenido.append(nodegraph)

        # Generar  endslice
        if(node.endslice is not None):
            self.visit(node.endslice)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.endslice._num)
            self.contenido.append(nodegraph)

    def visit_Container(self,node):
        nodegraph = '  node{} [label=<<B>Container</B> {} : in >]\n'.format( self.contador, node.item)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador + 1

        # Generar Conteiner
        self.visit(node.container)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.container._num)
        self.contenido.append(nodegraph)

    

    # EVALUACION
    def visit_EvalType(self,node):
        nodegraph = '  node{} [label=<<B>EvalType</B> : ::{} >]\n'.format( self.contador,node.type_data.identifier if isinstance(node.type_data,Identifier) else node.type_data)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar expression
        self.visit(node.expression)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.expression._num)
        self.contenido.append(nodegraph)



    # IDENTIFIER
    def visit_Identifier(self,node):
        nodegraph = '  node{} [label=<<B>Identifier</B> :{}>]\n'.format( self.contador , node.identifier )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1



    # NATIVE
    def visit_Native(self,node):
        nodegraph = '  node{} [label=<<B>Native</B> tipo: {}>]\n'.format(self.contador,node.typefunction)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar Parametros
        self.visit(node.parameters)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.parameters._num)
        self.contenido.append(nodegraph)



    # OPERATION
    def visit_Arithmetic(self,node):
        nodegraph = '  node{} [label=<<B>Arithmetic</B> : {} >]\n'.format( self.contador,node.op)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar left
        if node.left is not None:
            self.visit(node.left)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.contenido.append(nodegraph)

        # Generar right
        if node.right is not None:
            self.visit(node.right)
            nodegraph = '  node{} -> node{}\n'.format(node._num, node.right._num)
            self.contenido.append(nodegraph)

    def visit_Boolean(self,node):
        nodegraph = '  node{} [label="Boolean : {}" ]\n'.format( self.contador,node.op)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar left
        self.visit(node.left)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.left._num)
        self.contenido.append(nodegraph)

        # Generar right
        self.visit(node.right)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.right._num)
        self.contenido.append(nodegraph)

    def visit_UArithmetic(self, node):
        nodegraph = '  node{} [label=<<B>UArithmetic</B> : {} >]\n'.format( self.contador,node.op)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar val
        self.visit(node.val)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.val._num)
        self.contenido.append(nodegraph)

    def visit_UBoolean(self, node):
        nodegraph = '  node{} [label=<<B>UBoolean</B> : {} >]\n'.format( self.contador,node.op)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Generar val
        self.visit(node.val)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.val._num)



    # PARAMETER
    def visit_FormalParam(self,node):
        nodegraph = '  node{} [label=<( <B> Arguments </B> )>]\n'.format(self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador += 1
   
        for parametro in node.var_node:
            if(parametro is not None):
                if(isinstance(parametro,int) or isinstance(parametro,str) or isinstance(parametro,float) or isinstance(parametro,bool)):
                    nodeval = '  node{} [label=< <B> Def : </B> {} >]\n'.format(self.contador,parametro)
                    self.contenido.append(nodeval)   
                    nodeval = '  node{} -> node{}\n'.format(node._num, self.contador )
                    self.contenido.append(nodeval)
                    self.contador += 1
                else:
                    self.visit(parametro)
                    nodegraph = '  node{} -> node{}\n'.format(node._num, parametro._num)
                    self.contenido.append(nodegraph)



    # PRIMITIVE

    def visit_ValInteger(self,node):
        nodegraph = '  node{} [label=<<B>Int64</B> :{}>]\n'.format( self.contador , node.value )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

    def visit_ValFloat(self,node):
        nodegraph = '  node{} [label=<<B>Float64</B> :{}>]\n'.format( self.contador , node.value )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

    def visit_ValString(self,node):
        nodegraph = '  node{} [label=<<B>Cadena</B> :>]\n'.format( self.contador , )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        nodegraph = '  node{} [label="{}"]\n'.format( self.contador , node.value)
        self.contenido.append(nodegraph)
        nodegraph = '  node{} -> node{}\n'.format(node._num,self.contador)
        self.contenido.append(nodegraph)
        self.contador = self.contador +1



    def visit_ValCaracter(self,node):
        nodegraph = '  node{} [label=<<B>Char</B> :{}>]\n'.format( self.contador , node.value )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

    def visit_ValBool(self,node):
        nodegraph = '  node{} [label="<<B>Bool</B> :{}>"]\n'.format( self.contador , node.value )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

    def visit_ValNothing(self,node):
        nodegraph = '  node{} [label=<<B>Nothing</B> :{}>]\n'.format( self.contador , node.value )
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1


    


    # TRANSFERENCIA

    def visit_Return(self,node):
        nodegraph = '  node{} [label=<<B>Return</B>>]\n'.format( self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

        # Expression de Retorno
        self.visit(node.expression)
        nodegraph = '  node{} -> node{}\n'.format(node._num, node.expression._num)
        self.contenido.append(nodegraph) 

    def visit_Continue(self,node):
        nodegraph = '  node{} [label=<<B>Continue</B>>]\n'.format( self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1

    def visit_Break(self,node):
        nodegraph = '  node{} [label=<<B>Break</B>>]\n'.format( self.contador)
        self.contenido.append(nodegraph)
        node._num = self.contador
        self.contador = self.contador +1


    