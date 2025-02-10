import ply.lex as lex

# Lista de tokens
tokens = [
    'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING',  # Identificadores y literales
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',  # Operadores aritméticos
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',  # Operadores relacionales
    'ASSIGN',  # Operador de asignación
    'AND', 'OR', 'NOT',  # Operadores lógicos
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',  # Paréntesis, llaves y corchetes
    'COMMA', 'SEMICOLON', 'DOT',  # Otros símbolos
    'COMMENT_SHARP', 'CHARACTER_UNKNOWN', 'INVALID_HEX'  # Otros errores específicos
]

# Palabras reservadas
reserved = {
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'return': 'RETURN',
    'int': 'INT', 'float': 'FLOAT_K', 'char': 'CHAR', 'void': 'VOID'
}

tokens += list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='

t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

# Manejo de caracteres no reconocidos
def t_CHARACTER_UNKNOWN(t):
    r'[^\w\s\+\-\*/\(\)\[\]\{\},;=<>!\&\|\%\']'
    print(f"Error léxico: Carácter no reconocido '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)  # Saltar el carácter no reconocido

# Manejo de identificadores mal formados
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value[0].isdigit():
        print(f"Error léxico: Identificador mal formado '{t.value}' en línea {t.lexer.lineno}")
        t.value = ""  # Limpiar el valor del token
    else:
        t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Manejo de números flotantes incorrectos
def t_FLOAT(t):
    r'\d+\.\.\d+'
    print(f"Error léxico: Número flotante incorrecto '{t.value}' en línea {t.lexer.lineno}")
    t.value = ""  # Limpiar el valor del token
    return t

# Manejo de cadenas mal formadas
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    if t.value.count('"') % 2 == 1:  # Verifica si hay una comilla de cierre
        print(f"Error léxico: Cadena mal formada en línea {t.lexer.lineno}")
        t.value = ""  # Limpiar el valor del token
    else:
        t.value = t.value[1:-1]  # Remover comillas
    return t

# Manejo de comentarios mal cerrados
def t_COMMENT_SHARP(t):
    r'\#.*'
    pass

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    if t.value.startswith('/*') and not t.value.endswith('*/'):
        print(f"Error léxico: Comentario mal cerrado en línea {t.lexer.lineno}")
    pass

# Manejo de caracteres especiales no válidos (@)
def t_INVALID_CHAR(t):
    r'@'
    print(f"Error léxico: Uso de un carácter especial no válido '@' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Manejo de números con letras en medio
def t_INVALID_NUMBER(t):
    r'\d+[a-zA-Z]\d+'
    print(f"Error léxico: Uso de un número con una letra en medio '{t.value}' en línea {t.lexer.lineno}")
    t.value = ""  # Limpiar el valor del token
    return t

# Manejo de operadores desconocidos ($)
def t_UNKNOWN_OPERATOR(t):
    r'\$'
    print(f"Error léxico: Operador desconocido '$' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Manejo de punto y coma faltante
def t_SEMICOLON_MISSING(t):
    r'(?<=\w)\s*$'
    print(f"Error léxico: Falta punto y coma al final de la declaración en línea {t.lexer.lineno}")
    return t

# Manejo de uso incorrecto de secuencias de escape
def t_INVALID_ESCAPE_SEQUENCE(t):
    r'\\[^abfnrtv\\\'"]'
    print(f"Error léxico: Uso incorrecto de secuencias de escape en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Manejo de comillas simples en lugar de dobles en cadenas
def t_SINGLE_QUOTE_IN_STRING(t):
    r"'([^'\\]|\\.)*'"
    print(f"Error léxico: Uso de comillas simples en lugar de dobles en cadena de texto en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Manejo de números hexadecimales mal formados
def t_INVALID_HEX(t):
    r'\b[^0x0-9A-Fa-f]\d+[A-Fa-f0-9]{2,}\b'
    print(f"Error léxico: Número hexadecimal mal formado '{t.value}' en línea {t.lexer.lineno}")
    t.value = ""  # Limpiar el valor del token
    return t

# Manejo de comentarios con una sola barra (inválido)
def t_INVALID_SINGLE_SLASH_COMMENT(t):
    r'[^/]/.*'
    print(f"Error léxico: Comentario con una sola barra inclinada (inválido) en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores mejorado
def t_error(t):
    print(f"Error léxico: Carácter no reconocido '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
