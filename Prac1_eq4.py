# Este programa tiene como objetivo el dados n <= 20 y pares ordenados de x y y
# con consideraciones de i difrente de j para los sufijos de cada x y y, dar una sucesion
# de polinomios de Lagrange asociados a cada x, utilizando el metodo de Neville
# se uso POO ya que a pesar de ser un codigo mas grande, estoy aprendiendo a usarlo y siento
# que en este caso al quitar la recursividad y usandop clases es muchisimo mas legible en cada 
# parte, ya que se visualiza donde pasa cada parte del constructor, ademas que al ser tan explicito
# modular, pueden seguirse 'buenas practicas' al programar, y quita los problemas al cambiar la Big O
# del mismo programa que si se usaran ciclos anidados, ademas si se quiere manipular el programa
# es mas facil modificarlo en modulos sin temor a que deje de funcionar.

import sympy as sp
# Importamos sympy porque necesitamos construir y manipular expresiones simbólicas exactas

'Primera clase'
class InputHandler:
      # Esta clase es tal cual para crear objetos manipulables en los siguientes
      # con los inputs del usuario
      # Clase encargada de gestionar la entrada del usuario y validar:
      #           - n (entero positivo, n <= 20)
      #           - n+1 pares (x_i, y_i) con x_i distintos

      def leer_entero_n(self):
            # Lee y valida el entero n (n <= 20).
            # Retorna: int (n)

            while True:
                  raw = input("Introduce n (entero positivo, n <= 20): ").strip()
                  # Intentamos convertir a int; si falla, pedimos de nuevo.
                  try:
                        n = int(raw)
                        if n >= 0 and n <= 20:
                              return n
                        else:
                              print("El valor de n debe estar entre 0 y 20 (inclusive).")
                  except ValueError:
                        print("Entrada no válida. Introduce un entero.")
                    # todos los casos de n que pueden entrar excluyendo floats

      def leer_puntos(self, n):
            # Solicita al usuario n+1 pares (x, y).
            # Retorna dos listas: x_vals, y_vals (como strings limpias para luego convertir).
            # Es practicamente un creador de arrays con los datos que mete el usuario
            
            required = n + 1
            x_vals = []
            y_vals = []
            contador = 0
            while contador < required:
                  raw = input(f"Introduce el par #{contador} en formato x,y : ").strip()
                  # Separar por coma y validar formato básico
                  if ',' not in raw:
                        print("Formato incorrecto. Usa: x,y (por ejemplo: 1, 2/3 o 3.5, 4)")
                        continue
                  xs, ys = raw.split(',', 1)
                  xs = xs.strip()
                  ys = ys.strip()
                  # Comprobamos que x no se repita (comparación de strings por ahora)
                  if xs in x_vals:
                        print(f"El valor de x = {xs} ya fue ingresado. Los x deben ser distintos.")
                        continue
                  x_vals.append(xs)
                  y_vals.append(ys)
                  contador += 1
            return x_vals, y_vals

'Segunda clase'      
class PolinomioNeville:
      # Representa el polinomio interpolante construido por el método de Neville
      # Es importante recalcar que llama a los objetos de la primera clase para empezar
      # O armar, tipo constructor los polinmios interpolantes
      # sobre un conjunto de puntos (x, y).
      #       - La construcción se hace simbólicamente usando sympy.

      def __init__(self, x_syms, y_syms):
            # Inicialización: recibe listas de objetos simbólicos para x y y.
            
            self.x_syms = x_syms    
            self.y_syms = y_syms    
            self.x = sp.symbols('x')   # variable simbólica 'x' para construir expresiones
            self.polinomio = None
            # Construimos el polinomio simbólico al instanciar
            self.polinomio = self._construir_neville()

      def _construir_neville(self):
            # Construye la tabla triangular de Neville simbólicamente y retorna
            # P_{0,m}(x) donde m = len(x_syms)-1.
            # recuerden que len sirve para medir la longitud de un array o una cadena
            # Implementación: crea una matriz triangular (lista de listas) de expresiones sympy.

            m = len(self.x_syms)
            x = self.x

            # Inicializar tabla: P[i][i] = y_i

            P = [[None for _ in range(m)] for _ in range(m)]
            for i in range(m):
                  P = [[None for _ in range(m)] for _ in range(m)]
            for i in range(m):
                  P[i][i] = sp.simplify(self.y_syms[i])
            print("\nTabla de Neville simbólica:")
            print("-" * 60)
            for i in range(m):
                  print(f"P[{i},{i}] = {P[i][i]}")

            # Construcción iterativa de la tabla
            for span in range(1, m):  # span = j - i
                  for i in range(0, m - span):
                        j = i + span
                        xi = self.x_syms[i]
                        xj = self.x_syms[j]
                        num = (x - xi) * P[i + 1][j] - (x - xj) * P[i][j - 1]
                        den = xj - xi
                        P[i][j] = sp.simplify(num / den)
                        print(f"P[{i},{j}] = {P[i][j]}")

            print("-" * 60)
            print(f"Polinomio final P[0,{m - 1}](x) = {P[0][m - 1]}")
            print("-" * 60)

            return sp.simplify(P[0][m - 1])

      def mostrar(self):
            # Representaci[on simbolica
            return sp.simplify(self.polinomio)

      def evaluar(self, x_val):
            # Evalúa numéricamente el polinomio en x_val.
            # Tarea única: evaluación.
            return sp.N(self.polinomio.subs(self.x, x_val))


class InterpoladorNeville:
      # Clase ensambladora que:
      #      - Valida y convierte los datos de entrada a simbólicos exactos.
      #      - Genera la sucesión de polinomios P_1 ... P_n usando PolinomioNeville.

      def __init__(self, x_vals_raw, y_vals_raw):
            # solo prepara datos.

            self.x_raw = x_vals_raw
            self.y_raw = y_vals_raw
            # Convertir a objetos sympy (Rational si la entrada es exacta, si no usar sympify)
            self.x_syms = [self._to_sym(val) for val in self.x_raw]
            self.y_syms = [self._to_sym(val) for val in self.y_raw]
            # Validaciones
            self._validar_unicidad_x()
            self.n = len(self.x_syms) - 1
            self.polinomios = []   
            # lista donde guardaremos instancias de PolinomioNeville en nuevo array

      def _to_sym(self, s):
            # Intenta crear una Rational si la cadena es racional exacta (e.g. '3', '2/5'),
            # de lo contrario usa sympify para expresiones como '1.5' o 'sqrt(2)'.

            s = s.strip()
            # Intento 1: si es racional (contiene '/'), usar Rational
            if '/' in s:
                  try:
                        return sp.Rational(s)
                  except Exception:
                        # si falla, caemos a sympify
                        return sp.sympify(s)
            # Intento 2: si es entero
            try:
                  return sp.Integer(s)
            except Exception:
                  pass
            # Intento 3: si es decimal o expresión, usar sympify
            return sp.sympify(s)

      def _validar_unicidad_x(self):
            # Asegura que los x sean distintos (comparación simbólica).

            seen = set()
            for xi in self.x_syms:
                  # Convertimos la expresión simbólica a string canónica para comparar unicidad
                  key = str(sp.simplify(xi))
                  if key in seen:
                        raise ValueError(f"Valor de x repetido detectado: {xi}")
                  seen.add(key)

      def generar_sucesion(self):
            # Genera la sucesión de polinomios P_1 ... P_n.
            
            m = len(self.x_syms)
            # Para cada k = 1..n, construimos con los primeros k+1 puntos (índices 0..k)
            for k in range(1, m):
                  x_subset = self.x_syms[0:(k + 1)]
                  y_subset = self.y_syms[0:(k + 1)]
                  pol = PolinomioNeville(x_subset, y_subset)
                  self.polinomios.append(pol)

      def obtener_polinomios(self):
            # Retorna la lista de expresiones simbólicas simplificadas de P_1...P_n.
            
            return [p.mostrar() for p in self.polinomios]

      def mostrar_sucesion(self):
            # Tarea única: imprimir la sucesión en un formato legible.
            # Print por fin

            for idx, p in enumerate(self.polinomios, start=1):
                  expr = sp.simplify(p.mostrar())
                  print(f"P_{idx}(x) =")
                  # sympy.pretty_print podría usarse, pero usamos str(expr) para simplicidad
                  print(expr)
                  print("-" * 60)

def main():
      # Flujo principal de la aplicación:
      #      1) Pedir n
      #      2) Pedir los n+1 pares
      #      3) Construir interpolador
      #      4) Generar sucesión y mostrarla

      ih = InputHandler()                         # tarea: gestionar entrada
      n = ih.leer_entero_n()                      # tarea: leer y validar n
      x_raw, y_raw = ih.leer_puntos(n)           # tarea: leer pares (como strings)
      interpolador = InterpoladorNeville(x_raw, y_raw)  # tarea: convertir y validar simbólicamente
      interpolador.generar_sucesion()             # tarea: construir la sucesión con Neville
      interpolador.mostrar_sucesion()             # tarea: imprimir resultados


# Invocación segura de main
if __name__ == "__main__":
      main()

