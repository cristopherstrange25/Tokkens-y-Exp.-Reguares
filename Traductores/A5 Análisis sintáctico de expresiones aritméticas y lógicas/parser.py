import ply.yacc as yacc
from lexer import tokens

# Definir la precedencia de los operadores (para el análisis correcto de la aritmética)
precedence = (
    ('left', 'MAYOR', 'MENOR', 'IGUAL', 'DIFERENTE', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'AND', 'OR'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
)

# Regla de la gramática para las expresiones aritméticas y lógicas
def p_expresion(p):
    '''expresion : expresion_aritmetica
                 | expresion_logica'''
    p[0] = p[1]

def p_expresion_aritmetica(p):
    '''expresion_aritmetica : termino
                            | expresion_aritmetica MAS termino
                            | expresion_aritmetica MENOS termino'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_termino(p):
    '''termino : factor
              | termino POR factor
              | termino DIVIDIDO factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_factor(p):
    '''factor : NUMERO
              | IDENTIFICADOR
              | PARIZQ expresion_aritmetica PARDER'''
    if len(p) == 2:
        p[0] = int(p[1]) if isinstance(p[1], str) and p[1].isdigit() else p[1]
    elif len(p) == 4:
        p[0] = p[2]

def p_expresion_logica(p):
    '''expresion_logica : termino_logico
                       | expresion_logica AND termino_logico
                       | expresion_logica OR termino_logico'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]

def p_termino_logico(p):
    '''termino_logico : expresion_aritmetica IGUAL expresion_aritmetica
                     | expresion_aritmetica DIFERENTE expresion_aritmetica
                     | expresion_aritmetica MAYOR expresion_aritmetica
                     | expresion_aritmetica MENOR expresion_aritmetica
                     | expresion_aritmetica MAYORIGUAL expresion_aritmetica
                     | expresion_aritmetica MENORIGUAL expresion_aritmetica'''
    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error sintáctico: '{p.value}' en la línea {p.lineno}")
    else:
        print("Error sintáctico en la entrada.")

# Construir el parser
parser = yacc.yacc()



# Función para analizar código
def analizar_codigo(codigo):
    parser.parse(codigo)