
class Visitor:

    def execute(self,node):
        method_name = 'execute_' + type(node).__name__             # visit_nombredelaclaseAST 
        #  getattr se usa para obtener el valor del atributo de un objeto
        #  y si no se encuentra ningún atributo de ese objeto, se devuelve el valor predeterminado.
        execute = getattr(self, method_name, self.generic_visit) 
        # visitor sera el metodo de la instancia de lo contrario retornar el metodo generico
        return execute(node)

    def generic_execute(self, node):
        #pass                       #Para evitar generacion de excepciones
        raise Exception('No execute_{} method'.format(type(node).__name__))
    


class Tree:
    def __init__(self, row =None, col=None):
        self.row = row
        self.col = col
        
    def execute(self,tree,table):
        pass

    