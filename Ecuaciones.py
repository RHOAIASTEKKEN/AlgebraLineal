import sympy as sp
import tkinter as tk
from tkinter import messagebox, ttk
import re

class FractionalEquationSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Resolutor de Ecuaciones")
        self.master.geometry("700x500")  # Aumentamos el tamaño de la ventana

        # Contenedor con barra de desplazamiento
        self.canvas = tk.Canvas(master)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Etiqueta para instrucciones
        self.label_instrucciones = tk.Label(self.scrollable_frame, text="Ingrese la ecuación:")
        self.label_instrucciones.pack()

        # Entrada de ecuación
        self.ecuacion_input = tk.Entry(self.scrollable_frame, width=60)  # Aumentamos el ancho
        self.ecuacion_input.pack()

        # Botones para operaciones
        self.botones_frame = tk.Frame(self.scrollable_frame)
        self.botones_frame.pack()

        self.boton_1 = tk.Button(self.botones_frame, text="√", command=lambda: self.insertar_simbolo("sqrt("))
        self.boton_1.grid(row=0, column=0)

        self.boton_2 = tk.Button(self.botones_frame, text="^", command=lambda: self.insertar_simbolo("**"))
        self.boton_2.grid(row=0, column=1)

        self.boton_3 = tk.Button(self.botones_frame, text="/", command=lambda: self.insertar_simbolo("/"))
        self.boton_3.grid(row=0, column=2)

        self.boton_4 = tk.Button(self.botones_frame, text="(", command=lambda: self.insertar_simbolo("("))
        self.boton_4.grid(row=1, column=0)

        self.boton_5 = tk.Button(self.botones_frame, text=")", command=lambda: self.insertar_simbolo(")"))
        self.boton_5.grid(row=1, column=1)

        self.boton_6 = tk.Button(self.botones_frame, text="*", command=lambda: self.insertar_simbolo("*"))
        self.boton_6.grid(row=1, column=2)

        # Botón para resolver la ecuación
        self.resolver_button = tk.Button(self.scrollable_frame, text="Resolver Ecuación", command=self.resolver_ecuacion)
        self.resolver_button.pack()

        # Contenedor para mostrar los resultados
        self.resultados_frame = tk.Frame(self.scrollable_frame, width=680, height=300)  # Aumentamos el tamaño
        self.resultados_frame.pack(pady=10)
        self.resultados_frame.pack_propagate(False)  # Evita que el frame se encoja

        # Canvas para los resultados
        self.resultados_canvas = tk.Canvas(self.resultados_frame, width=660)
        self.resultados_canvas.pack(side="left", fill="both", expand=True)

        self.resultados_scrollbar = tk.Scrollbar(self.resultados_frame, orient="vertical", command=self.resultados_canvas.yview)
        self.resultados_scrollbar.pack(side="right", fill="y")

        self.resultados_inner_frame = ttk.Frame(self.resultados_canvas)

        self.resultados_inner_frame.bind(
            "<Configure>",
            lambda e: self.resultados_canvas.configure(
                scrollregion=self.resultados_canvas.bbox("all")
            )
        )

        self.resultados_canvas.create_window((0, 0), window=self.resultados_inner_frame, anchor="nw")
        self.resultados_canvas.configure(yscrollcommand=self.resultados_scrollbar.set)

        self.resultados_label = tk.Label(self.resultados_inner_frame, text="", justify="left", wraplength=640)  # Añadimos wraplength
        self.resultados_label.pack()

        # Botón para limpiar todo
        self.limpiar_button = tk.Button(self.scrollable_frame, text="Limpiar Todo", command=self.limpiar_todo)
        self.limpiar_button.pack()

    def insertar_simbolo(self, simbolo):
        """Inserta un símbolo o texto en la posición actual del cursor en la entrada de texto."""
        self.ecuacion_input.insert(tk.INSERT, simbolo)

    def resolver_ecuacion(self):
        ecuacion = self.ecuacion_input.get()

        # Reemplazar patrones de números seguidos de letras para agregar '*' automáticamente
        ecuacion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', ecuacion)

        try:
            # Convertir la ecuación de texto a una ecuación simbólica
            lhs, rhs = ecuacion.split("=")
            lhs_expr = sp.sympify(lhs.replace('^', '**'))
            rhs_expr = sp.sympify(rhs.replace('^', '**'))

            # Detectar las variables en la ecuación
            variables = lhs_expr.free_symbols.union(rhs_expr.free_symbols)

            if len(variables) < 1:
                messagebox.showerror("Error", "Por favor ingrese una ecuación con una o más variables.")
                return

            # Resolver la ecuación
            solucion = sp.solve(lhs_expr - rhs_expr, variables)

            if not solucion:
                messagebox.showerror("Error", "No se pudo encontrar una solución.")
                return

            # Filtrar las soluciones reales
            soluciones_reales = [sol.evalf() for sol in solucion if sol.is_real]
            soluciones_complejas = [sol.evalf() for sol in solucion if not sol.is_real]

            # Comprobación de la solución con detalles
            comprobacion_resultados = []
            for i, sol in enumerate(soluciones_reales):
                comprobacion = {}
                for var in variables:
                    # Sustituir en el lado izquierdo y derecho
                    lhs_val = lhs_expr.subs(var, sol)
                    rhs_val = rhs_expr.subs(var, sol)
                    comprobacion[var] = {
                        'sustitucion': f"{var} = {sol}",
                        'lhs': lhs_val.evalf(),
                        'rhs': rhs_val.evalf(),
                        'es_correcta': abs(lhs_val.evalf() - rhs_val.evalf()) < 1e-10
                    }
                comprobacion_resultados.append(comprobacion)

            # Generar el resultado con fracciones y decimales
            resultado_texto = ""
            if soluciones_reales:
                resultado_texto += f"Solución en fracciones:\n{solucion}\n\n"
                resultado_texto += f"Solución en decimales:\n{soluciones_reales}\n\n"
                resultado_texto += "Comprobación detallada:\n"
                for i, comprobacion in enumerate(comprobacion_resultados):
                    resultado_texto += f"Solución {i+1}:\n"
                    for var, detalles in comprobacion.items():
                        resultado_texto += f"  {detalles['sustitucion']}\n"
                        resultado_texto += f"    Lado Izquierdo = {detalles['lhs']}\n"
                        resultado_texto += f"     Lado Derecho = {detalles['rhs']}\n"
                        resultado_texto += f"    {'Correcta' if detalles['es_correcta'] else 'Incorrecta'}\n"
                    resultado_texto += "\n"
            else:
                resultado_texto += "No hay soluciones reales.\n\n"

            if soluciones_complejas:
                resultado_texto += f"Soluciones complejas:\n{soluciones_complejas}\n"

            # Mostrar resultados en el contenedor
            self.resultados_label.config(text=resultado_texto)

        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver la ecuación: {str(e)}")

    def limpiar_todo(self):
        """Limpia la entrada de la ecuación y los resultados."""
        self.ecuacion_input.delete(0, tk.END)
        self.resultados_label.config(text="")

# Configuración de la ventana principal
root = tk.Tk()
app = FractionalEquationSolver(root)

# Ingresar ecuaciones de prueba
app.ecuacion_input.insert(0, "(sqrt(a**2-3))/a=a-3/2")  # Pre-poblar la ecuación

root.mainloop()