from codeditor.jolc.jolc.Abstract.Node import Tree

'''
    InstructionList solo recibe una lista de parametros no ejecuta nada
    pero la clase sera util en la construccion del arbol de derivacion
'''
class InstructionList(Tree):
    def __init__(self, declarations=[]):
        self.declarations = declarations
    
    def execute(self, tree, table):
        return self

    def __str__(self):
       instrucciones = ''.join(map(str, self.declarations))
       return f'<InstructionList instrucciones: {instrucciones} >'

    