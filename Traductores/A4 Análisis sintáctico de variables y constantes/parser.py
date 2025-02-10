import ply.yacc as yacc
from lexer import tokens

valid_types = ['int', 'float', 'bool', 'char']  # Tipos válidos

# Declaración de una variable o constante
def p_declaration(p):
    '''
    declaration : variable_decl
                | constant_decl
    '''
    pass

# Declaración de una variable
def p_variable_decl(p):
    '''
    variable_decl : TYPE IDENTIFIER SEMICOLON
                  | TYPE IDENTIFIER ASSIGN literal SEMICOLON
    '''
    tipo = p[1]  # El tipo de la variable (ej. "float", "bool", etc.)
    nombre = p[2]  # El nombre de la variable
    linea = p.lineno(1)  # Línea donde ocurre

    # 🛑 Error 1: Comprobar si el tipo es válido
    if tipo not in valid_types:
        print(f"Error: Tipo no válido '{tipo}' en línea {linea}. Los tipos válidos son 'int', 'float', 'bool', 'char'.")
        return

    # 🛑 Error 2: Comprobar si el identificador es válido
    if not nombre.isidentifier():  # Verifica si el identificador es válido
        print(f"Error: Identificador no válido '{nombre}' en línea {linea}.")
        return

    # 🛑 Error 3: Comprobar la asignación y si el valor es un literal
    if len(p) > 4:  # Si hay una asignación
        valor_asignado = p[4]
        if not isinstance(valor_asignado, str):  # Solo se aceptan literales
            print(f"Error: Asignación inválida a '{nombre}' en línea {linea}. Solo se pueden asignar valores literales.")
            return

    print(f"Declaración válida de variable en línea {linea}")

# Declaración de una constante
def p_constant_decl(p):
    '''
    constant_decl : CONST TYPE IDENTIFIER ASSIGN literal SEMICOLON
    '''
    tipo = p[2]  # El tipo de la constante
    nombre = p[3]  # El nombre de la constante
    linea = p.lineno(1)

    # 🛑 Error 1: Comprobar si el tipo es válido
    if tipo not in valid_types:
        print(f"Error: Tipo no válido '{tipo}' en línea {linea}. Los tipos válidos son 'int', 'float', 'bool', 'char'.")
        return

    # 🛑 Error 2: Comprobar si el identificador es válido
    if not nombre.isidentifier():
        print(f"Error: Identificador no válido '{nombre}' en línea {linea}.")
        return

    print(f"Declaración válida de constante en línea {linea}")

# Literal (puede ser int, float, string, etc.)
def p_literal(p):
    '''
    literal : INT_LITERAL
            | FLOAT_LITERAL
            | STRING_LITERAL
            | BOOL_LITERAL
    '''
    pass

# Error de sintaxis
def p_error(p):
    if p:
        # Verificar errores específicos relacionados con la declaración
        if p.type == 'IDENTIFIER':
            print(f"Error: Identificador no válido '{p.value}' en línea {p.lineno}")
        elif p.type == 'TYPE' and p.value not in valid_types:
            print(f"Error: Tipo no válido '{p.value}' en línea {p.lineno}. Los tipos válidos son 'int', 'float', 'bool', 'char'.")
        elif p.type == 'SEMICOLON':
            print(f"Error: Falta ';' al final de la declaración en línea {p.lineno}")
        else:
            print(f"Error de sintaxis en '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo")

parser = yacc.yacc()


# Función para analizar código
def analizar_codigo(codigo):
    parser.parse(codigo)
