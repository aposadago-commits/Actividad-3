import math
import tkinter as tk
from tkinter import messagebox


class Notas:
    """Define una lista de cinco notas y sus cálculos."""

    def __init__(self):
        self.lista_notas = [0.0] * 5

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas)

    def calcular_desviacion(self):
        promedio = self.calcular_promedio()
        suma = sum(
            math.pow(nota - promedio, 2)
            for nota in self.lista_notas
        )
        return math.sqrt(suma / len(self.lista_notas))

    def calcular_mayor(self):
        return max(self.lista_notas)

    def calcular_menor(self):
        return min(self.lista_notas)


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notas")
        self.resizable(False, False)
        self._inicio()
        self._centrar()

    def _inicio(self):
        """Crea los componentes gráficos de la ventana."""
        marco = tk.Frame(self, padx=20, pady=15)
        marco.pack()

        self.campos_nota = []
        for i in range(5):
            tk.Label(marco, text=f"Nota {i + 1}:").grid(
                row=i,
                column=0,
                sticky="w",
                pady=3,
            )
            campo = tk.Entry(marco, width=18)
            campo.grid(row=i, column=1, pady=3, padx=(10, 0))
            self.campos_nota.append(campo)

        botones = tk.Frame(marco)
        botones.grid(row=5, column=0, columnspan=2, pady=12)

        tk.Button(
            botones,
            text="Calcular",
            width=10,
            command=self.calcular,
        ).pack(side="left", padx=5)
        tk.Button(
            botones,
            text="Limpiar",
            width=10,
            command=self.limpiar,
        ).pack(side="left", padx=5)

        self.promedio = tk.Label(marco, text="Promedio = ", anchor="w")
        self.desviacion = tk.Label(
            marco,
            text="Desviación estándar = ",
            anchor="w",
        )
        self.mayor = tk.Label(marco, text="Nota mayor = ", anchor="w")
        self.menor = tk.Label(marco, text="Nota menor = ", anchor="w")

        resultados = (
            self.promedio,
            self.desviacion,
            self.mayor,
            self.menor,
        )
        for fila, etiqueta in enumerate(resultados, start=6):
            etiqueta.grid(
                row=fila,
                column=0,
                columnspan=2,
                sticky="w",
                pady=2,
            )

    def _centrar(self):
        """Posiciona la ventana en el centro de la pantalla."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 3
        self.geometry(f"+{x}+{y}")

    def calcular(self):
        notas = Notas()

        for i, campo in enumerate(self.campos_nota):
            texto = campo.get().strip().replace(",", ".")
            if not texto:
                messagebox.showwarning(
                    "Dato faltante",
                    f"La nota {i + 1} no ha sido ingresada.\n"
                    "Es obligatorio ingresar las cinco notas.",
                )
                campo.focus_set()
                return

            try:
                valor = float(texto)
                if not math.isfinite(valor):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Dato no válido",
                    f"La nota {i + 1} debe ser un valor numérico.",
                )
                campo.focus_set()
                return

            notas.lista_notas[i] = valor

        self.promedio.config(
            text=f"Promedio = {notas.calcular_promedio():.2f}"
        )
        self.desviacion.config(
            text=(
                "Desviación estándar = "
                f"{notas.calcular_desviacion():.2f}"
            )
        )
        self.mayor.config(text=f"Nota mayor = {notas.calcular_mayor()}")
        self.menor.config(text=f"Nota menor = {notas.calcular_menor()}")

    def limpiar(self):
        for campo in self.campos_nota:
            campo.delete(0, tk.END)
        self.campos_nota[0].focus_set()


if __name__ == "__main__":
    VentanaPrincipal().mainloop()
