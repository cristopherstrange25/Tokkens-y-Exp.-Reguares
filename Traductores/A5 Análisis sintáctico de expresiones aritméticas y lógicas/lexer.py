import ply.lex as lex
import ply.yacc as yacc

# Definición de los tokens
tokens = (
    'IDENTIFICADOR', 'NUMERO', 'MAS', 'MENOS', 'POR', 'DIVIDIDO',
    'PARIZQ', 'PARDER', 'IGUAL', 'DIFERENTE', 'MAYOR', 'MENOR',
    'MAYORIGUAL', 'MENORIGUAL', 'AND', 'OR', 'COMA'
)

# Expresiones regulares para los tokens
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_COMA = r','

# Identificadores (variables)
t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Números (enteros)
t_NUMERO = r'\d+'

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print(f"Error léxico: {t.value} en la línea {t.lineno}, columna {t.lexpos}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

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

# Función para analizar las expresiones y manejar errores
def analizar_expresion(expresion):
    try:
        lexer.input(expresion)
        parser.parse(expresion)
        return "Expresión inválida"
    except:
        return "Error en la expresión"

# Lista de expresiones inválidas
expresiones_invalidas = [
    "x + * y",    # Operador sin término
    "10 >",       # Comparación sin expresión aritmética
    "(a - b",     # Paréntesis desbalanceados
    "5 / (2 + )", # Paréntesis desbalanceados
]

# Imprimir las expresiones inválidas con sus errores
print("//Expresiones inválidas:")
for expr in expresiones_invalidas:
    print(f"{expr}  // {analizar_expresion(expr)}")
