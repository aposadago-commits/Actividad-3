import math
import tkinter as tk
from tkinter import messagebox

class FiguraGeometrica:
    def __init__(self):
        self._volumen = 0.0
        self._superficie = 0.0

    @property
    def volumen(self):
        return self._volumen

    @volumen.setter
    def volumen(self, valor):
        self._volumen = valor

    @property
    def superficie(self):
        return self._superficie

    @superficie.setter
    def superficie(self, valor):
        self._superficie = valor

    def _actualizar(self):
        self.volumen = self.calcular_volumen()
        self.superficie = self.calcular_superficie()


class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        super().__init__()
        self.radio = radio
        self.altura = altura
        self._actualizar()

    def calcular_volumen(self):
        return math.pi * self.altura * math.pow(self.radio, 2.0)

    def calcular_superficie(self):
        area_lado_a = 2.0 * math.pi * self.radio * self.altura
        area_lado_b = 2.0 * math.pi * math.pow(self.radio, 2.0)
        return area_lado_a + area_lado_b


class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        super().__init__()
        self.radio = radio
        self._actualizar()

    def calcular_volumen(self):
        # El libro usa 1.333; aquí se usa 4/3 exacto.
        return (4.0 / 3.0) * math.pi * math.pow(self.radio, 3.0)

    def calcular_superficie(self):
        return 4.0 * math.pi * math.pow(self.radio, 2.0)


class Piramide(FiguraGeometrica):
    def __init__(self, base, altura, apotema):
        super().__init__()
        self.base = base
        self.altura = altura
        self.apotema = apotema
        self._actualizar()

    def calcular_volumen(self):
        return (math.pow(self.base, 2.0) * self.altura) / 3.0

    def calcular_superficie(self):
        area_base = math.pow(self.base, 2.0)
        area_lados = 2.0 * self.base * self.apotema
        return area_base + area_lados


class Cubo(FiguraGeometrica):         
    def __init__(self, arista):
        super().__init__()
        self.arista = arista
        self._actualizar()

    def calcular_volumen(self):
        return math.pow(self.arista, 3.0)

    def calcular_superficie(self):
        return 6.0 * math.pow(self.arista, 2.0)


class Prisma(FiguraGeometrica):      
    def __init__(self, largo, ancho, altura):
        super().__init__()
        self.largo = largo
        self.ancho = ancho
        self.altura = altura
        self._actualizar()

    def calcular_volumen(self):
        return self.largo * self.ancho * self.altura

    def calcular_superficie(self):
        return 2.0 * (self.largo * self.ancho
                      + self.largo * self.altura
                      + self.ancho * self.altura)

def _centrar(ventana):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ventana.winfo_width()) // 2
    y = (ventana.winfo_screenheight() - ventana.winfo_height()) // 3
    ventana.geometry(f"+{x}+{y}")


class VentanaFigura(tk.Toplevel):
   
    titulo = ""
    campos = ()   

    def __init__(self, padre):
        super().__init__(padre)
        self.title(self.titulo)
        self.resizable(False, False)
        marco = tk.Frame(self, padx=20, pady=15)
        marco.pack()

        self.entradas = []
        for i, nombre in enumerate(self.campos):
            tk.Label(marco, text=f"{nombre} (cms):").grid(
                row=i, column=0, sticky="w", pady=3)
            entrada = tk.Entry(marco, width=16)
            entrada.grid(row=i, column=1, pady=3, padx=(10, 0))
            self.entradas.append(entrada)

        tk.Button(marco, text="Calcular", width=16,
                  command=self.calcular).grid(
            row=len(self.campos), column=1, pady=10, padx=(10, 0))

        self.volumen = tk.Label(marco, text="Volumen (cm3):", anchor="w")
        self.superficie = tk.Label(marco, text="Superficie (cm2):",
                                   anchor="w")
        self.volumen.grid(row=len(self.campos) + 1, column=0, columnspan=2,
                          sticky="w", pady=2)
        self.superficie.grid(row=len(self.campos) + 2, column=0,
                             columnspan=2, sticky="w", pady=2)
        _centrar(self)

    def crear_figura(self, valores):
        raise NotImplementedError

    def calcular(self):
        try:
            valores = [float(e.get().replace(",", ".")) for e in self.entradas]
            if any(not math.isfinite(v) for v in valores):
                raise ValueError
            figura = self.crear_figura(valores)
            self.volumen.config(
                text=f"Volumen (cm3): {figura.calcular_volumen():.2f}")
            self.superficie.config(
                text=f"Superficie (cm2): {figura.calcular_superficie():.2f}")
        except ValueError:      # campo vacío o texto que no es un número
            messagebox.showerror("Error",
                                 "Campo nulo o error en formato de número",
                                 parent=self)


class VentanaCilindro(VentanaFigura):
    titulo = "Cilindro"
    campos = ("Radio", "Altura")

    def crear_figura(self, v):
        return Cilindro(*v)


class VentanaEsfera(VentanaFigura):
    titulo = "Esfera"
    campos = ("Radio",)

    def crear_figura(self, v):
        return Esfera(*v)


class VentanaPiramide(VentanaFigura):
    titulo = "Pirámide"
    campos = ("Base", "Altura", "Apotema")

    def crear_figura(self, v):
        return Piramide(*v)


class VentanaCubo(VentanaFigura):      
    titulo = "Cubo"
    campos = ("Arista",)

    def crear_figura(self, v):
        return Cubo(*v)


class VentanaPrisma(VentanaFigura):    
    titulo = "Prisma"
    campos = ("Largo", "Ancho", "Altura")

    def crear_figura(self, v):
        return Prisma(*v)


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Figuras")
        self.resizable(False, False)
        marco = tk.Frame(self, padx=20, pady=30)
        marco.pack()
        botones = (("Cilindro", VentanaCilindro), ("Esfera", VentanaEsfera),
                   ("Pirámide", VentanaPiramide), ("Cubo", VentanaCubo),
                   ("Prisma", VentanaPrisma))
        for texto, clase_ventana in botones:
            tk.Button(marco, text=texto, width=9,
                      command=lambda c=clase_ventana: c(self)
                      ).pack(side="left", padx=4)
        _centrar(self)

if __name__ == "__main__":
    VentanaPrincipal().mainloop()