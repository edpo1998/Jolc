from django.http import HttpResponse    # Librebiar para peticiones
from django.shortcuts import render     # Libreria para renderizar en el DOM
from codeditor.jolc import jolc         # Interprete de JOLC
from codeditor.jolc.jolc.ASTVisualizer import ASTVisualizer 
from django.conf import settings

import graphviz

# Create your views here.


# Variable Global de Las vistas que tendra los valores de cada ejecucion
# No se recomienda pero para fines practicos es funcional

context = {
        "code": '',
        "output":'',
        "ast":'',
        "tablesym": [],
        "tablerror":[],
        }




# Renderiza la pantalla principal (la vista se encuentra en el template)
def home_view(request, *args, **kwargs):
    context["code"] = ''
    context["output"] = ''
    context["ast"] = ''
    context["tablesym"] = []
    context["tablerror"] = []
    return  render(request, "home.html",{} )




# Renderiza la vista del editor de codigo 
def codeditor(request, *args, **kwargs):
    
    if request.method == "GET":
        '''
            El metodo GET se llama cada vez que se actualiza la pagina 
            debido a que se llama para extraer archivos de utilidad en este caso
            archivos de imagenes locales y los archivos de utilidad de codemirror
        '''
        pass
    else:
        '''
             El metodo POST se llama cuando hay envios en el request (Envio reciente o Reenvio)
             es importante hace notar que cada vez que se renderiza la pagina se producen metodos  
             get para extraer archivos locales o archivos de utilidad en el proyecto 
        '''
        context['code'] = request.POST['code']    #  Actualizamos la variable global por el post del editor
        ast = jolc.execute(context['code'])       #  Ejecutamos el Interprete de jolc 
        if(ast.output is not None):
            context['output'] = ast.output            #  Salidas generadas por la ejecucion del interprete
            context['tablerror'] = ast.errores        #  Tabla de errores de la ejecucion
            context['tablesym'] =  ast.tablasimbolos  #  Tabla de simbolos de la ejecucion
            context['ast'] = ast
        else:
            context['output'] = "Excepcion Ocurrida"

    return  render( request , "codeditor/editor.html", context)



#   Renderiza el Menu de Reportes
def report(request, *args, **kwargs):
    return  render( request , "codeditor/report.html", {})

#   Renderiza la Tabla de erroes
def bugreport(request, *args, **kwargs):
    return  render( request , "codeditor/bugreport.html", {"tabla": context['tablerror'] })

#   Renderiza la Tabla de simbolos
def symbolreport(request, *args, **kwargs):
    return  render( request , "codeditor/symbolreport.html", {"tabla": context['tablesym']})

#   Renderiza el arbol ast y lo almacena en la aplicacion como un archivo estatico
def treereport(request, *args, **kwargs):
    dot = ASTVisualizer(context['ast'])
    reporte   = dot.GenereteAst()         #  Ast generado por la derivacion de la gramatica  
    ast = graphviz.Source(reporte)
    ast.view();
    #ast.render(tree_url, view=True)     
    return  render( request , "codeditor/report.html", {})