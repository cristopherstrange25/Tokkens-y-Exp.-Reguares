import ply.lex as lex
import ply.yacc as yacc

# Definir los tokens
tokens = (
    'IF', 'ELSE', 'WHILE', 'FOR', 'IDENTIFICADOR', 'NUMERO', 'MAS', 'MENOS', 'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER', 'PUNTOYCOMA',
)

# Expresiones regulares de los tokens
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_FOR = r'for'
t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMERO = r'\d+'
t_MAS = r'\+'
t_MENOS = r'-'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PUNTOYCOMA = r';'

# Ignorar espacios en blanco
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Error de estructura de control: {t.value} en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definir las reglas del parser
def p_estructura_control(p):
    '''estructura_control : sentencia_if
                          | sentencia_while
                          | sentencia_for'''
    p[0] = p[1]

def p_sentencia_if(p):
    '''sentencia_if : IF PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER
                    | IF PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER ELSE LLAVEIZQ bloque LLAVEDER'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], p[10])

def p_sentencia_while(p):
    '''sentencia_while : WHILE PARIZQ expresion PARDER LLAVEIZQ bloque LLAVEDER'''
    p[0] = ('while', p[3], p[6])

def p_sentencia_for(p):
    '''sentencia_for : FOR PARIZQ asignacion PUNTOYCOMA expresion PUNTOYCOMA expresion PARDER LLAVEIZQ bloque LLAVEDER'''
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_bloque(p):
    '''bloque : sentencia
             | bloque sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_asignacion(p):
    '''asignacion : IDENTIFICADOR MAS NUMERO
                  | IDENTIFICADOR MENOS NUMERO'''
    p[0] = (p[1], p[2], p[3])

def p_expresion(p):
    '''expresion : IDENTIFICADOR
                 | NUMERO'''
    p[0] = p[1]

def p_sentencia(p):
    '''sentencia : asignacion PUNTOYCOMA'''
    p[0] = p[1]

def p_error(p):
    print(f"Error de estructura de control: '{p.value}' en la línea {p.lineno}" if p else "Error de estructura de control en la entrada.")

# Construir el parser
parser = yacc.yacc()

# Función para analizar código
def analizar_codigo(codigo):
    parser.parse(codigo)

# Casos de prueba
codigo_valido = """
if (x > 0) { x = x + 1; } else { x = x - 1; }
while (y < 10) { y = y + 1; }
for (i = 0; i < 10; i = i + 1) { suma = suma + i; }
"""

codigo_invalido = """
if (x > 0 { x = x + 1; }  
while x < 10) { y = y + 1; }  
for i = 0; i < 10; i = i + 1) { suma = suma + i; }  
"""



print("\nAnalizando código inválido:")
analizar_codigo(codigo_invalido)