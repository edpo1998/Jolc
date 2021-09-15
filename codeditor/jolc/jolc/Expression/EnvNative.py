import   math 
from   codeditor.jolc.jolc.Error import Description

class FuncNative:
    def __init__(self,val1=None,val2=None):
        self.val1 = val1    # A
        self.val2 = val2    # B

    def execute(self,method_name): 
        visitor = getattr(self, 'native_' + method_name, self.generic_visit) 
        # visitor sera el metodo de la instancia de lo contrario retornar el metodo generico que devuelve None
        return visitor()

    def generic_visit(self, node):
        return None

    def native_sin(self):
        return math.sin(self.val1)

    def native_cos(self):
        return math.cos(self.val1)
    
    def native_tan(self):
        return math.tan(self.val1)
    
    def native_sqrt(self):
        return math.sqrt(self.val1)
    
    def native_log10(self):
        return math.log10(self.val1)

    def native_uppercase(self):
        return str.upper(self.val1)

    def native_lowercase(self):
        return str.lower(self.val1)

    def native_float(self):
        return float(self.val1)

    def native_string(self):
        return str(self.val1)


    def native_typeof(self):
        return type(self.val1)

    def native_length(self):
        return len(self.val1)

    def native_pushno(self):
        return self.val1.append(self.val2)

    def native_popno(self):
        return self.val1.pop()

    def native_log(self):
        return math.log(self.val2,self.val1)

    def native_parse(self):
        print(self.val1)
        print(self.val2)
        if(self.val1 == 'Float64'):
            return float(self.val2)
        elif(self.val1 == 'Int64'):
            return int(self.val2)
        else:
            return int(self.val1) 

    def native_trunc(self):
        if(self.val1 == 'Int64'):
            return math.trunc(self.val2)
        if(self.val1 == 'Float64'):
            return math.trunc(self.val2)
        else:
            return math.trunc(self.val1) 
