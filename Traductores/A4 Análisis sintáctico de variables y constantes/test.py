from parser import parser

# Casos de prueba
pruebas = [
    "int x;",
    "float y;",
    "bool activo;",
    "char nombre;",
    "int 123x;",  # Identificador no válido
    "flotante y;",  # Tipo no válido
    "bool activo",  # Falta punto y coma
    "char 123;",  # Identificador no válido
]

for prueba in pruebas:
    print(f"Probando: {prueba}")
    parser.parse(prueba)
    print()