import sympy as sp
import tkinter as tk
from tkinter import messagebox
import re

class EquationSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Resolutor de Ecuaciones")

        # Listas para almacenar las ecuaciones y restricciones
        self.ecuaciones = []
        self.restricciones = []

        # Etiquetas y entradas para las ecuaciones
        self.label_ecuacion = tk.Label(master, text="Ingrese la ecuación (ej: 5x + 3y = 12300):")
        self.label_ecuacion.pack()
        self.ecuacion_input = tk.Entry(master, width=40)
        self.ecuacion_input.pack()

        # Botón para agregar la ecuación
        self.agregar_ecuacion_button = tk.Button(master, text="Agregar Ecuación", command=self.agregar_ecuacion)
        self.agregar_ecuacion_button.pack()

        # Etiquetas y entradas para las restricciones
        self.label_restriccion = tk.Label(master, text="Ingrese una restricción (ej: x = 1/2 * y):")
        self.label_restriccion.pack()
        self.restriccion_input = tk.Entry(master, width=40)
        self.restriccion_input.pack()

        # Botón para agregar la restricción
        self.agregar_restriccion_button = tk.Button(master, text="Agregar Restricción", command=self.agregar_restriccion)
        self.agregar_restriccion_button.pack()

        # Botón para resolver las ecuaciones
        self.resolver_button = tk.Button(master, text="Resolver Ecuaciones", command=self.resolver_ecuaciones)
        self.resolver_button.pack()

        # Botón para limpiar todo
        self.limpiar_button = tk.Button(master, text="Limpiar Todo", command=self.limpiar_todo)
        self.limpiar_button.pack()

        # Crear un Canvas para visualizar los resultados
        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack()

    def convertir_expresiones(self, expresion):
        # Reemplazar expresiones como 5x o 3y por 5*x o 3*y
        # También maneja la notación fraccionaria como "1/2"
        expresion = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expresion)
        expresion = expresion.replace("de", "*")  # Cambiar "de" por "*"
        return expresion

    def agregar_ecuacion(self):
        ecuacion = self.ecuacion_input.get()
        if ecuacion.strip():
            ecuacion_convertida = self.convertir_expresiones(ecuacion)
            self.ecuaciones.append(ecuacion_convertida)
            self.ecuacion_input.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Ecuación agregada. Total de ecuaciones: " + str(len(self.ecuaciones)))
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una ecuación válida.")

    def agregar_restriccion(self):
        restriccion = self.restriccion_input.get()
        if restriccion.strip():
            restriccion_convertida = self.convertir_expresiones(restriccion)
            self.restricciones.append(restriccion_convertida)
            self.restriccion_input.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Restricción agregada. Total de restricciones: " + str(len(self.restricciones)))
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una restricción válida.")

    def limpiar_todo(self):
        self.ecuaciones.clear()
        self.restricciones.clear()
        self.canvas.delete("all")  # Limpiar el canvas
        messagebox.showinfo("Limpiar", "Se han limpiado todas las ecuaciones y restricciones.")

    def resolver_ecuaciones(self):
        if not self.ecuaciones or not self.restricciones:
            messagebox.showwarning("Advertencia", "Asegúrese de agregar al menos una ecuación y una restricción.")
            return

        try:
            # Detectar variables utilizadas
            variables = set()
            for ecuacion in self.ecuaciones + self.restricciones:
                for simbolo in ecuacion:
                    if simbolo.isalpha():
                        variables.add(simbolo)

            # Definir las variables dinámicamente
            variable_dict = {var: sp.symbols(var) for var in variables}

            sistema = []
            for ecuacion in self.ecuaciones:
                if '=' in ecuacion:
                    lhs, rhs = ecuacion.split('=')
                    sistema.append(sp.sympify(lhs, locals=variable_dict) - sp.sympify(rhs, locals=variable_dict))
                else:
                    sistema.append(sp.sympify(ecuacion, locals=variable_dict))

            # Agregar restricciones como ecuaciones
            for restriccion in self.restricciones:
                if '=' in restriccion:
                    lhs, rhs = restriccion.split('=')
                    sistema.append(sp.sympify(lhs, locals=variable_dict) - sp.sympify(rhs, locals=variable_dict))

            # Resolver el sistema
            solucion = sp.solve(sistema, list(variable_dict.values()))

            if not solucion:
                messagebox.showerror("Error", "No se pudo encontrar una solución.")
                return

            # Generar resultados
            resultado_fracciones = "Resultados en fracciones:\n" + "\n".join(f"{var} = {solucion[var]}" for var in variable_dict.values())
            resultado_decimales = "Resultados en decimales:\n" + "\n".join(f"{var} = {float(solucion[var])}" for var in variable_dict.values())

            # Comprobación de las ecuaciones
            comprobacion = []
            for ecuacion in self.ecuaciones:
                ecuacion_sympy = sp.sympify(ecuacion.split('=')[0], locals=variable_dict) - sp.sympify(ecuacion.split('=')[1], locals=variable_dict)
                if all([ecuacion_sympy.subs(solucion).simplify() == 0]):
                    comprobacion.append(f"✅ {ecuacion}")
                else:
                    comprobacion.append(f"❌ {ecuacion}")

            for restriccion in self.restricciones:
                restriccion_sympy = sp.sympify(restriccion.split('=')[0], locals=variable_dict) - sp.sympify(restriccion.split('=')[1], locals=variable_dict)
                if all([restriccion_sympy.subs(solucion).simplify() == 0]):
                    comprobacion.append(f"✅ {restriccion}")
                else:
                    comprobacion.append(f"❌ {restriccion}")

            comprobacion_texto = "\nComprobación:\n" + "\n".join(comprobacion)

            # Limpiar el canvas y mostrar resultados
            self.canvas.delete("all")  # Limpiar el canvas
            y_offset = 20  # Desplazamiento inicial para el texto
            
            # Mostrar resultados en fracciones
            self.canvas.create_text(10, y_offset, anchor='nw', text=resultado_fracciones, font=('Arial', 12))
            y_offset += 20 * (len(variable_dict) + 1)  # Ajustar el desplazamiento según el número de variables

            # Mostrar resultados en decimales
            self.canvas.create_text(10, y_offset, anchor='nw', text=resultado_decimales, font=('Arial', 12))
            y_offset += 20 * (len(variable_dict) + 1)  # Ajustar el desplazamiento según el número de variables

            # Mostrar comprobación
            self.canvas.create_text(10, y_offset, anchor='nw', text=comprobacion_texto, font=('Arial', 12))

        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver las ecuaciones: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolver(root)
    root.mainloop()
