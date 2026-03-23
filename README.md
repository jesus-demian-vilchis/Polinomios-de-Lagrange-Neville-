# Neville Interpolation with SymPy

Este programa implementa el método de Neville para la interpolación polinómica. Dado un conjunto de puntos (x_i, y_i) con i = 0..n (n <= 20), el programa genera la sucesión de polinomios de Lagrange asociados a cada x_i, utilizando el método de Neville de forma iterativa. La implementación está orientada a objetos, empleando la biblioteca SymPy para el manejo simbólico exacto de las expresiones.

## Características

- Solicita al usuario el valor de `n` (número de puntos menos uno, con n ≤ 20) y los n+1 pares (x_i, y_i).
- Valida que los valores de x sean distintos y que n esté en el rango permitido.
- Construye de forma simbólica la tabla de Neville, mostrando cada paso intermedio.
- Genera la sucesión de polinomios P_1(x), P_2(x), ..., P_n(x) (cada uno interpolando los primeros k+1 puntos).
- Muestra cada polinomio en forma simplificada.
- Permite evaluar numéricamente cualquier polinomio resultante (aunque no se usa en la salida principal).

## Requisitos

- Python 3.6 o superior.
- SymPy (biblioteca para matemática simbólica).

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/neville-interpolation.git
   cd neville-interpolation
