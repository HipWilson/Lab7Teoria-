# Laboratorio 7 - Teoria de la computacion
# Problema 1: validacion de gramaticas y eliminacion de producciones-ε
import os
import re
import sys

# Cuerpo de produccion: ε o una cadena de letras y digitos
CUERPO = r'(?:ε|[A-Za-z0-9]+)'
# Linea valida: Mayuscula → cuerpo | cuerpo | ...
PATRON = re.compile(r'^[A-Z]\s*(?:→|->)\s*' + CUERPO + r'(?:\s*\|\s*' + CUERPO + r')*$')


def cargar_gramatica(ruta):
    # Devuelve {'S': [('0','A','0'), ...]} y el simbolo inicial. Cuerpo vacio () = ε
    gramatica = {}
    inicial = None

    with open(ruta, encoding='utf-8') as f:
        lineas = f.readlines()

    for numero, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if linea == '':
            continue

        if not PATRON.match(linea):
            print(f'ERROR en la linea {numero}: "{linea}"')
            print('La linea no cumple el formato:  X → cuerpo | cuerpo | ...')
            print('Ejecucion detenida.')
            sys.exit(1)

        cabeza, cuerpos = re.split(r'→|->', linea)
        cabeza = cabeza.strip()
        if inicial is None:
            inicial = cabeza
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


def encontrar_anulables(gramatica):
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
                # anulable si el cuerpo es ε o todos sus simbolos ya son anulables
                if all(s in anulables for s in cuerpo):
                    nuevos.append(cabeza)
                    print(f'  Iteracion {iteracion}: {cabeza} es anulable '
                          f'(por {cabeza} → {cuerpo_a_texto(cuerpo)})')
                    break
        for n in nuevos:
            anulables.add(n)
            cambio = True
    print(f'  Conjunto de anulables = {{{", ".join(sorted(anulables))}}}')
    return anulables


def generar_combinaciones(cuerpo, anulables):
    # Genera los 2^m casos de quitar o dejar cada simbolo anulable
    posiciones = [i for i, s in enumerate(cuerpo) if s in anulables]
    m = len(posiciones)
    resultado = []
    for mascara in range(2 ** m):
        quitar = set()
        for j in range(m):
            if (mascara >> j) & 1:
                quitar.add(posiciones[j])
        nuevo = tuple(s for i, s in enumerate(cuerpo) if i not in quitar)
        resultado.append(nuevo)
    return resultado, m


def eliminar_epsilon(gramatica, inicial):
    print('\n=== PASO 1: Encontrar simbolos anulables ===')
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
                    print('      caso ε -> se descarta')
                elif c in nueva[cabeza]:
                    print(f'      caso {cuerpo_a_texto(c)} -> ya existe')
                else:
                    nueva[cabeza].append(c)
                    print(f'      caso {cuerpo_a_texto(c)} -> se agrega')

    if inicial in anulables:
        print(f'\n  Nota: el simbolo inicial {inicial} era anulable, '
              f'asi que ε ya no pertenece al lenguaje de la nueva gramatica.')
    return nueva


def ejecutar(ruta):
    print('\n' + '=' * 60)
    print(f'Archivo: {os.path.basename(ruta)}')
    print('=' * 60)

    gramatica, inicial = cargar_gramatica(ruta)

    print(f'\nGramatica leida correctamente (simbolo inicial: {inicial}):')
    mostrar_gramatica(gramatica)

    resultado = eliminar_epsilon(gramatica, inicial)

    print('\n=== RESULTADO: Gramatica sin producciones-ε ===')
    mostrar_gramatica(resultado)


def main():
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gramaticas')

    if not os.path.isdir(carpeta):
        print('No se encontro la carpeta "gramaticas".')
        sys.exit(1)

    archivos = sorted(f for f in os.listdir(carpeta) if f.endswith('.txt'))
    if len(archivos) == 0:
        print('No hay archivos .txt en la carpeta "gramaticas".')
        sys.exit(1)

    while True:
        print('\n===== ELIMINACION DE PRODUCCIONES-ε =====')
        print('Elige la gramatica a ejecutar:')
        for i, nombre in enumerate(archivos, start=1):
            print(f'  {i}. {nombre}')
        print('  0. Salir')

        opcion = input('\nNumero de opcion: ').strip()

        if opcion == '0':
            print('Programa terminado.')
            break
        if not opcion.isdigit() or not (1 <= int(opcion) <= len(archivos)):
            print('Opcion no valida, intenta de nuevo.')
            continue

        # si el archivo tiene errores, cargar_gramatica detiene el programa
        ejecutar(os.path.join(carpeta, archivos[int(opcion) - 1]))

        input('\nPresiona Enter para volver al menu...')


main()