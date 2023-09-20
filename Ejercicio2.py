import re

# Función para validar si una línea de producción es válida
def es_linea_valida(linea):
    patron_produccion = r'^[A-Z]\s*->\s*([A-Za-z0-9ε]+(\s*\|\s*[A-Za-z0-9ε]+)*)?$'

    # ^           # Start of the string
    # [A-Z]       # Single uppercase letter as LHS
    # \s*         # Optional whitespace
    # ->          # Arrow symbol
    # \s*         # Optional whitespace
    # (           # Start of RHS group
    #     [A-Za-z0-9ε]+      # One or more alphanumeric characters or ε
    #     (                   # Start of optional alternations
    #         \s*             # Optional whitespace
    #         \|              # Pipe symbol for alternations
    #         \s*             # Optional whitespace
    #         [A-Za-z0-9ε]+  # One or more alphanumeric characters or ε
    #     )*                  # End of optional alternations (zero or more)
    # )?          # End of RHS group (optional)
    # $           # End of the string
    return re.match(patron_produccion, linea) is not None

# Función para cargar una gramática desde un archivo de texto
def cargar_gramatica(archivo):
    gramatica = {}
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()  # Eliminar espacios en blanco al inicio y final
                if es_linea_valida(linea):
                    lhs, rhs = map(str.strip, linea.split('->'))
                    producciones = [p.strip() for p in rhs.split('|')]
                    gramatica[lhs] = producciones
                else:
                    print(f"Error: Línea inválida en el archivo: {linea}")
                    return None
        return gramatica
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {archivo}")
        return None

# Función para eliminar producciones-𝜀
def simplificar_gramatica(gramatica):
    gramatica_simplificada = gramatica.copy()

    # Eliminar producciones vacías
    gramatica_simplificada = {k: v for k, v in gramatica_simplificada.items() if v}

    # Eliminar reglas inaccesibles
    reglas_accesibles = set()
    pila = ["S"]
    while pila:
        regla = pila.pop()
        reglas_accesibles.add(regla)
        for produccion in gramatica_simplificada.get(regla, []):
            for simbolo in produccion:
                if simbolo not in reglas_accesibles and simbolo in gramatica_simplificada:
                    pila.append(simbolo)

    gramatica_simplificada = {k: v for k, v in gramatica_simplificada.items() if k in reglas_accesibles}

    # Eliminar producciones unitarias
    producciones_unitarias_a_eliminar = []
    for regla, producciones in gramatica_simplificada.items():
        for produccion in producciones:
            if len(produccion) == 1 and produccion[0] in gramatica_simplificada:
                producciones_unitarias_a_eliminar.append((regla, produccion))

    for regla, produccion in producciones_unitarias_a_eliminar:
        gramatica_simplificada[regla].remove(produccion)

    # Fusionar producciones idénticas
    for regla, producciones in gramatica_simplificada.items():
        producciones_unicas = set()
        for produccion in producciones:
            producciones_unicas.add(''.join(produccion))
        gramatica_simplificada[regla] = list(producciones_unicas)

    return gramatica_simplificada

# Función para imprimir la gramática resultante
def imprimir_gramatica(gramatica):
    for lhs, producciones in gramatica.items():
        producciones_str = ' | '.join(producciones)
        print(f"{lhs} -> {producciones_str}")

# Cargar una gramática desde un archivo de texto
nombre_archivo = 'data.txt'  
mi_gramatica = cargar_gramatica(nombre_archivo)

if mi_gramatica is not None:
    # Eliminar producciones-𝜀 de la gramática
    mi_gramatica = simplificar_gramatica(mi_gramatica)

    # Imprimir la gramática resultante
    imprimir_gramatica(mi_gramatica)
