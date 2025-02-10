import ply.yacc as yacc
from lexer import lexer

# Definición de la gramática y reglas del parser
def p_estructura_control(p):
    '''estructura_control : sentencia_if
                          | sentencia_while
                          | sentencia_for'''
    p[0] = p[1]

def p_sentencia_if(p):
    '''sentencia_if : IF PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER
                    | IF PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER ELSE LLAVEIZQ bloque LLAVEDER'''
    if len(p) == 9:
        p[0] = ('if', p[3], p[6])  # ('if', condición, bloque)
    elif len(p) == 13:
        p[0] = ('if', p[3], p[6], p[10])  # ('if', condición, bloque, else_bloque)

def p_sentencia_while(p):
    '''sentencia_while : WHILE PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER'''
    p[0] = ('while', p[3], p[6])  # ('while', condición, bloque)

def p_sentencia_for(p):
    '''sentencia_for : FOR PARIZQ inicializacion PUNTOYCOMA expresion PUNTOYCOMA actualizacion PARDER LLAVEIZQ bloque LLAVEDER'''
    p[0] = ('for', p[3], p[5], p[7], p[10])  # ('for', inicialización, condición, actualización, bloque)

def p_bloque(p):
    '''bloque : sentencia
             | bloque sentencia'''
    p[0] = p[1:]  # Almacena las sentencias del bloque

def p_sentencia(p):
    '''sentencia : expresion
                 | estructura_control
                 | declaracion
                 | asignacion'''
    p[0] = p[1]

def p_expresion(p):
    '''expresion : IDENTIFICADOR
                 | NUMERO'''
    p[0] = p[1]

def p_inicializacion(p):
    '''inicializacion : declaracion
                      | asignacion'''
    p[0] = p[1]

def p_actualizacion(p):
    '''actualizacion : expresion'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Error sintáctico: '{p.value}' en la línea {p.lineno}")
    else:
        print("Error sintáctico en la entrada.")

# Construir el parser
parser = yacc.yacc()

# Función para analizar código
def analizar_codigo(codigo):
    try:
        parser.parse(codigo)
        print("Código válido")
    except Exception as e:
        print(f"Error de sintaxis: {e}")
