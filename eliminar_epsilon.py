# Laboratorio 7 - Teoría de la computación
# Problema 1: Carga de gramáticas, validación con regex y eliminación de producciones-ε
import re
import sys

# ---------------------------------------------------------------
# 1. EXPRESIÓN REGULAR PARA VALIDAR CADA LÍNEA
# ---------------------------------------------------------------
# Un cuerpo de producción es: ε  o  una cadena de letras/dígitos (ej: 0A0, BB, aAa)
CUERPO = r'(?:ε|[A-Za-z0-9]+)'
# Línea completa: Mayúscula  →  cuerpo  ( | cuerpo )*
PATRON = re.compile(r'^[A-Z]\s*(?:→|->)\s*' + CUERPO + r'(?:\s*\|\s*' + CUERPO + r')*$')


def cargar_gramatica(ruta):
    """Lee el archivo, valida cada línea con la regex y devuelve la gramática.
    La gramática es un diccionario: {'S': [('0','A','0'), ('B','B')], ...}
    Un cuerpo vacío () representa ε.
    Si una línea está mal escrita, el programa se detiene."""
    gramatica = {}
    inicial = None

    with open(ruta, encoding='utf-8') as f:
        lineas = f.readlines()

    for numero, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if linea == '':
            continue  # se ignoran líneas en blanco

        if not PATRON.match(linea):
            print(f'ERROR en la línea {numero}: "{linea}"')
            print('La línea no cumple el formato:  X → cuerpo | cuerpo | ...')
            print('Ejecución detenida.')
            sys.exit(1)

        # separar cabeza y cuerpos
        cabeza, cuerpos = re.split(r'→|->', linea)
        cabeza = cabeza.strip()
        if inicial is None:
            inicial = cabeza  # el primer no terminal es el símbolo inicial
        if cabeza not in gramatica:
            gramatica[cabeza] = []

        for cuerpo in cuerpos.split('|'):
            cuerpo = cuerpo.strip()
            simbolos = () if cuerpo == 'ε' else tuple(cuerpo)
            if simbolos not in gramatica[cabeza]:
                gramatica[cabeza].append(simbolos)

    return gramatica, inicial


def cuerpo_a_texto(cuerpo):
    return 'ε' if len(cuerpo) == 0 else ''.join(cuerpo)


def mostrar_gramatica(gramatica):
    for cabeza, cuerpos in gramatica.items():
        texto = ' | '.join(cuerpo_a_texto(c) for c in cuerpos)
        print(f'  {cabeza} → {texto}')


# ---------------------------------------------------------------
# 2. ELIMINACIÓN DE PRODUCCIONES-ε
# ---------------------------------------------------------------
def encontrar_anulables(gramatica):
    """Paso 1: encontrar los símbolos anulables (los que derivan en ε)."""
    anulables = set()
    iteracion = 0
    cambio = True
    while cambio:
        cambio = False
        iteracion += 1
        nuevos = []
        for cabeza, cuerpos in gramatica.items():
            if cabeza in anulables:
                continue
            for cuerpo in cuerpos:
                # anulable si el cuerpo es ε o si TODOS sus símbolos ya son anulables
                if all(s in anulables for s in cuerpo):
                    nuevos.append(cabeza)
                    print(f'  Iteración {iteracion}: {cabeza} es anulable '
                          f'(por {cabeza} → {cuerpo_a_texto(cuerpo)})')
                    break
        for n in nuevos:
            anulables.add(n)
            cambio = True
    print(f'  Conjunto de anulables = {{{", ".join(sorted(anulables))}}}')
    return anulables


def generar_combinaciones(cuerpo, anulables):
    """Genera las 2^m combinaciones quitando/dejando cada símbolo anulable."""
    posiciones = [i for i, s in enumerate(cuerpo) if s in anulables]
    m = len(posiciones)
    resultado = []
    for mascara in range(2 ** m):
        quitar = set()
        for j in range(m):
            if (mascara >> j) & 1:      # si el bit j es 1, se quita ese símbolo
                quitar.add(posiciones[j])
        nuevo = tuple(s for i, s in enumerate(cuerpo) if i not in quitar)
        resultado.append(nuevo)
    return resultado, m


def eliminar_epsilon(gramatica, inicial):
    print('\n=== PASO 1: Encontrar símbolos anulables ===')
    anulables = encontrar_anulables(gramatica)

    print('\n=== PASO 2: Generar nuevas producciones (2^m casos) ===')
    nueva = {}
    for cabeza, cuerpos in gramatica.items():
        nueva[cabeza] = []
        for cuerpo in cuerpos:
            if len(cuerpo) == 0:
                print(f'  {cabeza} → ε  : se elimina')
                continue
            combinaciones, m = generar_combinaciones(cuerpo, anulables)
            if m == 0:
                print(f'  {cabeza} → {cuerpo_a_texto(cuerpo)}  : no tiene anulables, se mantiene')
            else:
                print(f'  {cabeza} → {cuerpo_a_texto(cuerpo)}  : {m} anulable(s), 2^{m} = {2**m} casos')
            for c in combinaciones:
                if len(c) == 0:
                    print(f'      caso ε -> se descarta')
                elif c in nueva[cabeza]:
                    print(f'      caso {cuerpo_a_texto(c)} -> ya existe')
                else:
                    nueva[cabeza].append(c)
                    print(f'      caso {cuerpo_a_texto(c)} -> se agrega')

    if inicial in anulables:
        print(f'\n  Nota: el símbolo inicial {inicial} era anulable, '
              f'así que ε ya no pertenece al lenguaje de la nueva gramática.')
    return nueva


# ---------------------------------------------------------------
# 3. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
    else:
        ruta = input('Nombre del archivo de la gramática: ').strip()

    try:
        gramatica, inicial = cargar_gramatica(ruta)
    except FileNotFoundError:
        print(f'No se encontró el archivo "{ruta}".')
        sys.exit(1)

    print(f'\nGramática leída correctamente (símbolo inicial: {inicial}):')
    mostrar_gramatica(gramatica)

    resultado = eliminar_epsilon(gramatica, inicial)

    print('\n=== RESULTADO: Gramática sin producciones-ε ===')
    mostrar_gramatica(resultado)


main()
