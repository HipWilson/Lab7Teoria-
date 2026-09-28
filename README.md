# Laboratorio 7 - Teoría de la computación

**Autor:** Wilson Peña - 24760

## Video de demostración (Problema 1)
[(Link del video)](https://youtu.be/iupQoLKB3PM) 

## Ramas del repositorio
Cada problema está en su propia rama:

| Rama | Contenido |
|------|-----------|
| [`problema1`](../../tree/problema1) | Programa en Python: validación de gramáticas con regex y eliminación de producciones-ε. |
| [`problema2`](../../tree/problema2) | PDF con el procedimiento completo de las 3 CFGs (ε, unarias, inútiles y CNF). |

## Problema 1: Eliminación de producciones-ε
Programa en Python 3 que carga una gramática desde un archivo de texto, valida cada línea con una
expresión regular y elimina las producciones-ε mostrando cada paso en pantalla.

### Estructura de la rama `problema1`
```
├── eliminar_epsilon.py
└── gramaticas/
    ├── gramatica1.txt
    ├── gramatica2.txt
    ├── gramatica3.txt
    └── gramatica_error.txt   (contiene errores a propósito para mostrar la validación)
```

### Cómo ejecutarlo
```
git checkout problema1
python eliminar_epsilon.py
```
Se muestra un menú con las gramáticas de la carpeta `gramaticas/`. Al escribir el número de opción,
el algoritmo se ejecuta automáticamente con esa gramática.
```
1. gramatica1.txt
2. gramatica2.txt
3. gramatica3.txt
4. gramatica_error.txt   (detiene la ejecución por errores de formato)
0. Salir
```

### Formato de los archivos de gramática
- Una producción por línea; varios cuerpos separados por `|`.
- Mayúscula = no terminal, minúscula o dígito = terminal, `ε` = cadena vacía.
- Ejemplo: `S → 0A0 | 1B1 | BB`
- El primer no terminal del archivo es el símbolo inicial.

### Expresión regular de validación
`^[A-Z]\s*(?:→|->)\s*(?:ε|[A-Za-z0-9]+)(?:\s*\|\s*(?:ε|[A-Za-z0-9]+))*$`

Si una línea no la cumple, el programa muestra el número de línea y detiene la ejecución.

### Algoritmo
1. Buscar los símbolos anulables, iterando hasta que no haya cambios.
2. Para cada producción con m símbolos anulables, generar los 2^m casos; se descartan ε y los duplicados.
3. Mostrar la gramática resultante sin producciones-ε.

## Problema 2
Las respuestas con el procedimiento completo están en la rama [`problema2`](../../tree/problema2),
archivo `Problema2_Respuestas.pdf`.
