# Proyectos de Resolución de Ecuaciones

Este repositorio contiene dos scripts de Python para resolver ecuaciones utilizando una interfaz gráfica de usuario (GUI). Ambos scripts utilizan la biblioteca Tkinter para la GUI y SymPy para matemáticas simbólicas.

## 1. EcuacionesLineales.py

Este script proporciona una GUI para resolver sistemas de ecuaciones lineales con restricciones adicionales.

### Características:

- Agregar múltiples ecuaciones lineales
- Agregar restricciones al sistema
- Resolver el sistema de ecuaciones
- Mostrar resultados tanto en forma de fracción como decimal
- Verificar y mostrar la corrección de cada ecuación y restricción
- Limpiar todas las ecuaciones y restricciones

### Uso:

1. Ejecutar el script
2. Ingresar ecuaciones lineales en el formato "5x + 3y = 12300"
3. Agregar restricciones si es necesario (por ejemplo, "x = 1/2 \* y")
4. Hacer clic en "Resolver Ecuaciones" para resolver el sistema
5. Ver los resultados y la verificación en el área del canvas

## 2. Ecuaciones.py

Este script proporciona una GUI para resolver ecuaciones individuales, incluyendo ecuaciones con fracciones y funciones matemáticas.

### Características:

- Interfaz de usuario amigable con botones para símbolos matemáticos comunes
- Resolver ecuaciones con una o más variables
- Mostrar soluciones en forma de fracción y decimal
- Verificación detallada de las soluciones
- Manejar soluciones reales y complejas
- Limpiar la entrada y los resultados

### Uso:

1. Ejecutar el script
2. Ingresar la ecuación utilizando el teclado y los botones proporcionados
3. Hacer clic en "Resolver Ecuación" para obtener la solución
4. Ver los resultados detallados, incluyendo la verificación de la solución

## Requisitos

- Python 3.x
- Tkinter (generalmente incluido con Python)
- SymPy (`pip install sympy`)
- `sympy`
- `tkinter` (incluido por defecto en la mayoría de las instalaciones de Python)

Para instalar las bibliotecas necesarias, puedes usar el siguiente comando:

```bash
pip install -r requirements.txt
```

Comando para iniciar el env
```
.env\Scripts\activate 
```

## Ejecución

Para ejecutar cualquiera de los scripts, use el siguiente comando en la terminal:

## Notas

- Asegúrese de tener todas las dependencias instaladas antes de ejecutar los scripts.
- Para ecuaciones más complejas, el tiempo de resolución puede variar.