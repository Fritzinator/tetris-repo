import tkinter as tk
import random

class KoordinatenRasterGUI:
    def __init__(self, master, breite, höhe, feld_größe):
        self.master = master
        self.breite = breite
        self.höhe = höhe
        self.feld_größe = feld_größe
        self.raster = [[None for _ in range(breite)] for _ in range(höhe)]
        self.aktuelles_quadrat = None
        self.aktuelle_position = None

        self.canvas = tk.Canvas(master, width=breite*(feld_größe+1), height=höhe*(feld_größe+1))
        self.canvas.pack()

        for i in range(breite + 1):
            self.canvas.create_line(i*(feld_größe+1), 0, i*(feld_größe+1), höhe*(feld_größe+1), fill="black")
        for j in range(höhe + 1):
            self.canvas.create_line(0, j*(feld_größe+1), breite*(feld_größe+1), j*(feld_größe+1), fill="black")

        self.neues_quadrat()

        self.master.bind("<Left>", lambda event: self.bewege_links())
        self.master.bind("<Right>", lambda event: self.bewege_rechts())

    def neues_quadrat(self):
        x = random.randint(0, self.breite - 1)
        y = 0
        if self.raster[y][x] is None:
            self.aktuelles_quadrat = self.canvas.create_rectangle(x*(self.feld_größe+1), y*(self.feld_größe+1), (x+1)*(self.feld_größe+1), (y+1)*(self.feld_größe+1), fill="blue")
            self.raster[y][x] = self.aktuelles_quadrat
            self.aktuelle_position = (x, y)

        self.bewege_quadrat()

    def bewege_quadrat(self):
        x, y = self.aktuelle_position
        if y == self.höhe - 1 or self.raster[y+1][x] is not None:
            self.prüfe_reihe_voll()  # Überprüfe, ob eine Reihe vollständig ist
            self.neues_quadrat()  # Starte ein neues Quadrat oben
            return
        self.raster[y][x] = None
        self.raster[y+1][x] = self.aktuelles_quadrat
        self.aktuelle_position = (x, y+1)
        self.canvas.move(self.aktuelles_quadrat, 0, self.feld_größe+1)
        self.canvas.after(500, self.bewege_quadrat)

    def prüfe_reihe_voll(self):
        for y in range(self.höhe):
            if all(self.raster[y]):
                for x in range(self.breite):
                    if self.canvas.coords(self.raster[y][x])[3] < self.höhe*(self.feld_größe+1):  # Überprüfe, ob der Stein noch oben ist
                        return
                self.lösche_reihe(y)

    def lösche_reihe(self, reihe):
        for x in range(self.breite):
            self.canvas.delete(self.raster[reihe][x])
            self.raster[reihe][x] = None
        self.quadrat_rutschen(reihe)

    def quadrat_rutschen(self, reihe):
        for y in range(reihe-1, -1, -1):
            for x in range(self.breite):
                if self.raster[y][x] is not None:
                    quadrat_id = self.raster[y][x]
                    self.raster[y][x] = None
                    self.raster[y+1][x] = quadrat_id
                    self.canvas.move(quadrat_id, 0, (self.feld_größe+1))

    def bewege_links(self):
        x, y = self.aktuelle_position
        if x > 0 and self.raster[y][x-1] is None:
            self.raster[y][x] = None
            self.raster[y][x-1] = self.aktuelles_quadrat
            self.aktuelle_position = (x-1, y)
            self.canvas.move(self.aktuelles_quadrat, -self.feld_größe-1, 0)

    def bewege_rechts(self):
        x, y = self.aktuelle_position
        if x < self.breite - 1 and self.raster[y][x+1] is None:
            self.raster[y][x] = None
            self.raster[y][x+1] = self.aktuelles_quadrat
            self.aktuelle_position = (x+1, y)
            self.canvas.move(self.aktuelles_quadrat, self.feld_größe+1, 0)

# Beispiel Nutzung
root = tk.Tk()
root.title("Koordinatenraster mit fallenden Quadraten")
raster_gui = KoordinatenRasterGUI(root, 10, 10, 40)
root.mainloop()
