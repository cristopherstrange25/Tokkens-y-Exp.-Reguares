from parser import analizar_codigo

# Función para leer el archivo de código fuente
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        codigo = archivo.read()
    return codigo

# Ejemplo de uso
codigo = leer_archivo('tests\example.c')  # Ajusta la ruta según sea necesario
analizar_codigo(codigo)
