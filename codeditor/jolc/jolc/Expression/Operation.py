
from codeditor.jolc.jolc.Error import Description
from codeditor.jolc.jolc.Abstract.Node import Tree

class Operation(Tree):
    def __init__(self, left, op, right,row = None, col =None):
        super().__init__(row=row, col=col) 
        self.left = left
        self.op = op
        self.right = right
        

class UnaryOperation(Tree):
    def __init__(self, op, val,row = None, col =None):
        super().__init__(row=row, col=col) 
        self.op = op
        self.val = val


class Arithmetic(Operation):
    def __init__(self, left=None, op=None, right=None, row=None, col=None):
        super().__init__(left, op, right, row=row, col=col)

    def __str__(self):
        return f'<Arithmetic exp:{self.left} op: {self.op}  exp: {self.right} >'

    def execute(self, tree, table):
        expleft  = self.left.execute(tree,table)    #Extraemos valor izquierdo
        expright = self.right.execute(tree,table)   #Extraemos valor derecho
                 #Extraemos el operador
        # Si no devuelve nada entonces encadenar Error Semantico
        if(expleft is None or expright is None):
            tree.addError(Description.SEMANTIC_AEVAL,'exp',self.row,self.col)
            
        # De lo contrario realizar operacion validando el tipo del valor
        else:
            if self.op == '+':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft + expright
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            elif self.op == '-':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft - expright
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            elif self.op == '*':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft * expright
                elif isinstance(expleft,str) and isinstance(expright,str) :
                    return expleft + expright  
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            elif self.op== '/':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft / expright
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            elif self.op == '%':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft % expright
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            elif self.op== '^':
                if ((isinstance(expleft,int) or isinstance(expleft,float)) and (isinstance(expright,int) or isinstance(expright,float))):
                    return expleft ** expright
                elif isinstance(expleft,str) and isinstance(expright,int) :
                    return expleft * expright                   
                else:
                    tree.addError(Description.SEMANTIC_EVAL_ATIPO,'exp',self.row,self.col)
                    return None
            else:    
                tree.addError(Description.SEMANTIC_OPERATOR_AINVALID,'op',self.row,self.col)
                return None

class UArithmetic(UnaryOperation):
    def __init__(self, op=None, val=None, row=None, col=None):
        super().__init__(op, val, row=row, col=col)

    def execute(self, tree, table):
        exp = self.val.execute(tree, table)
        # Si no devuelve encadenar Error Semantico
        if(exp is None):
            tree.addError(Description.SEMANTIC_UNARY_AEVAL,'exp',self.row,self.col)
            return None
        else:
            if self.op == '+':
                if ((isinstance(exp,int) or isinstance(exp,float))):
                    return exp
                else:
                    tree.addError(Description.SEMANTIC_EVAL_TAUNARY,'+exp',self.row,self.col)
                    return None 
            elif self.op == '-':
                if ((isinstance(exp,int) or isinstance(exp,float))):
                    return -1 * exp
                else:
                    tree.addError(Description.SEMANTIC_EVAL_TAUNARY,'-exp',self.row,self.col)
                    return None  
            else:    
                tree.addError(Description.SEMANTIC_OPERATOR_AINVALID,'op',self.row,self.col)
                return None
        
    def __str__(self):
        return f'<UArithmetic op: {self.op}  val: {self.val} >'

class Boolean(Operation):
    def __init__(self, left=None, op=None, right=None, row=None, col=None):
        super().__init__(left, op, right, row=row, col=col)
    def __str__(self):
        return f'<Boolean exp:{self.left} op: {self.op}  exp: {self.right} >'
    def execute(self, tree, table):
        expleft  = self.left.execute(tree,table)   #Extraemos valor izquierdo
        expright = self.right.execute(tree,table)  #Extraemos valor derecho
        if self.op == '>':
            return  expleft > expright
        elif self.op  == '<':
            return  expleft < expright
        elif self.op  == '>=':
            return  expleft >= expright
        elif self.op  == '<=':
            return  expleft <= expright
        elif self.op  == '==':
            return  expleft == expright
        elif self.op  == '!=':
            return  expleft != expright
        elif self.op  == '&&':
            return  expleft and expright
        elif self.op  == '||':
            return  expleft or expright
        else:
            tree.addError(Description.SEMANTIC_OPERADOR_RINVALID,'rel log',self.row,self.col)

class UBoolean(UnaryOperation):
    def __init__(self, op=None, val=None, row=None, col=None):
        super().__init__(op, val, row=row, col=col)
    
    def execute(self, tree, table):
        exp = self.val.execute(tree.table)
        if(exp is None):
            tree.addError(Description.SEMANTIC_UNARY_BELVA,'!exp',self.row,self.col)
            return None
        else:
            if self.op == '!':
                if(isinstance(exp,bool)):
                    return not exp
                else:
                    tree.addError(Description.SEMANTIC_EVAL_TBUNARY,'type',self.row,self.col)
            else:
               tree.addError(Description.SEMANTIC_OPERATOR_BINVALID,'op',self.row,self.col) 

    def __str__(self):
        return f'<UBoolean op: {self.op}  val: {self.val} >'