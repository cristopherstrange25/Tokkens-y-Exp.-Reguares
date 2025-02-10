from lexer import lexer

def main():
    # Leer el archivo de prueba
    with open('C:/Users/user/Desktop/traductores/Lex-main/tests/example.c', 'r') as f:
        code = f.read()

    # Alimentar el lexer
    lexer.input(code)

    # Mostrar tokens generados
    print("Tokens encontrados:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

if __name__ == '__main__':
    main()
