import tkinter as tk
import random

class KoordinatenRasterGUI:
    def __init__(self, master, breite, höhe, feld_größe):
        self.master = master
        self.breite = breite
        self.höhe = höhe
        self.feld_größe = feld_größe
        self.raster = [[None for _ in range(breite)] for _ in range(höhe)]

        self.canvas = tk.Canvas(master, width=breite*(feld_größe+1), height=höhe*(feld_größe+1))
        self.canvas.pack()

        for i in range(breite + 1):
            self.canvas.create_line(i*(feld_größe+1), 0, i*(feld_größe+1), höhe*(feld_größe+1), fill="black")
        for j in range(höhe + 1):
            self.canvas.create_line(0, j*(feld_größe+1), breite*(feld_größe+1), j*(feld_größe+1), fill="black")

        self.neues_quadrat()

    def neues_quadrat(self):
        x = random.randint(0, self.breite - 1)
        y = 0
        if self.raster[y][x] is None:
            self.raster[y][x] = self.canvas.create_rectangle(x*(self.feld_größe+1), y*(self.feld_größe+1), (x+1)*(self.feld_größe+1), (y+1)*(self.feld_größe+1), fill="blue")

        self.bewege_quadrat(x, y)

    def bewege_quadrat(self, x, y):
        if y == self.höhe - 1 or self.raster[y+1][x] is not None:
            self.prüfe_reihe_voll()  # Überprüfe, ob eine Reihe vollständig ist
            self.neues_quadrat()  # Starte ein neues Quadrat oben
            return
        self.raster[y][x] = None
        self.raster[y+1][x] = self.canvas.find_closest((x+0.5)*(self.feld_größe+1), (y+1.5)*(self.feld_größe+1))[0]
        self.canvas.move(self.raster[y+1][x], 0, self.feld_größe+1)
        self.canvas.after(500, self.bewege_quadrat, x, y+1)

    def prüfe_reihe_voll(self):
        if all(self.raster[self.höhe - 1]):
            for x in range(self.breite):
                self.canvas.delete(self.raster[self.höhe - 1][x])
                self.raster[self.höhe - 1][x] = None
            self.quadrat_rutschen()

    def quadrat_rutschen(self):
        for y in range(self.höhe - 1, 0, -1):
            for x in range(self.breite):
                self.raster[y][x] = self.raster[y-1][x]
                if self.raster[y][x] is not None:
                    self.canvas.move(self.raster[y][x], 0, self.feld_größe+1)
                    self.raster[y-1][x] = None

# Beispiel Nutzung
root = tk.Tk()
root.title("Koordinatenraster mit fallenden Quadraten")
raster_gui = KoordinatenRasterGUI(root, 10, 10, 40)
root.mainloop()
