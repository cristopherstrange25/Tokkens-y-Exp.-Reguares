import ply.lex as lex

# Definir los tokens
tokens = (
    'TYPE', 'IDENTIFIER', 'INT_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL',
    'BOOL_LITERAL', 'CONST', 'ASSIGN', 'SEMICOLON'
)

# Definir las expresiones regulares para los tokens
t_TYPE = r'int|float|bool|char'
t_CONST = r'const'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_INT_LITERAL = r'\d+'
t_FLOAT_LITERAL = r'\d+\.\d+'
t_STRING_LITERAL = r'\"[^\"]*\"'
t_BOOL_LITERAL = r'true|false'

# Para los identificadores (solo letras y números, pero no puede empezar con un número)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in ('int', 'float', 'bool', 'char', 'const', 'true', 'false'):
        t.type = 'TYPE'  # Cambiar tipo si se encuentra una palabra reservada
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Error: Caracter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()
