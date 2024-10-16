import tkinter as tk
import random

tetrominos = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
    [(0, 0), (0, 1), (0, 2), (1, 2)],  # L
    [(0, 0), (0, 1), (0, 2), (-1, 2)], # Reverse L
    [(0, 0), (0, 1), (1, 1), (1, 2)],  # S
    [(0, 0), (0, 1), (-1, 1), (-1, 2)],# Z
    [(0, 0), (1, 0), (2, 0), (1, 1)]   # T
]

class TetrisGUI:
    def __init__(self, master, breite, höhe, feld_größe):
        self.master = master
        self.breite = breite
        self.höhe = höhe
        self.feld_größe = feld_größe
        self.raster = [[None for _ in range(breite)] for _ in range(höhe)]
        self.aktuelles_tetromino = None
        self.aktuelle_position = None
        self.tetromino_ids = []

        self.canvas = tk.Canvas(master, width=breite*(feld_größe+1), height=höhe*(feld_größe+1))
        self.canvas.pack()

        for i in range(breite + 1):
            self.canvas.create_line(i*(feld_größe+1), 0, i*(feld_größe+1), höhe*(feld_größe+1), fill="black")
        for j in range(höhe + 1):
            self.canvas.create_line(0, j*(feld_größe+1), breite*(feld_größe+1), j*(feld_größe+1), fill="black")

        self.neues_tetromino()

        self.master.bind("<Left>", lambda event: self.bewege_links())
        self.master.bind("<Right>", lambda event: self.bewege_rechts())
        self.master.bind("<Down>", lambda event: self.bewege_unten())
        self.master.bind("<Up>", lambda event: self.drehe_tetromino())

    def neues_tetromino(self):
        self.aktuelles_tetromino = random.choice(tetrominos)
        self.aktuelle_position = (self.breite // 2, 1)  # Start position
        self.tetromino_ids = []
        for x, y in self.aktuelles_tetromino:
            id = self.canvas.create_rectangle((self.aktuelle_position[0] + x) * (self.feld_größe + 1), 
                                              (self.aktuelle_position[1] + y) * (self.feld_größe + 1), 
                                              (self.aktuelle_position[0] + x + 1) * (self.feld_größe + 1), 
                                              (self.aktuelle_position[1] + y + 1) * (self.feld_größe + 1), 
                                              fill="blue")
            self.tetromino_ids.append(id)
        self.bewege_tetromino()

    def bewege_tetromino(self):
        if self.kann_bewegen(0, 1):
            self.aktuelle_position = (self.aktuelle_position[0], self.aktuelle_position[1] + 1)
            for id in self.tetromino_ids:
                self.canvas.move(id, 0, self.feld_größe + 1)
            self.master.after(500, self.bewege_tetromino)
        else:
            self.verschmelze_tetromino()
            self.prüfe_reihe_voll()
            self.neues_tetromino()

    def kann_bewegen(self, dx, dy):
        for x, y in self.aktuelles_tetromino:
            new_x = self.aktuelle_position[0] + x + dx
            new_y = self.aktuelle_position[1] + y + dy
            if new_x < 0 or new_x >= self.breite or new_y >= self.höhe or self.raster[new_y][new_x] is not None:
                return False
        return True

    def verschmelze_tetromino(self):
        for (x, y), id in zip(self.aktuelles_tetromino, self.tetromino_ids):
            self.raster[self.aktuelle_position[1] + y][self.aktuelle_position[0] + x] = id

    def prüfe_reihe_voll(self):
        for y in range(self.höhe):
            if all(self.raster[y]):
                for x in range(self.breite):
                    self.canvas.delete(self.raster[y][x])
                    self.raster[y][x] = None
                self.quadrat_rutschen(y)

    def quadrat_rutschen(self, reihe):
        for y in range(reihe-1, -1, -1):
            for x in range(self.breite):
                if self.raster[y][x] is not None:
                    quadrat_id = self.raster[y][x]
                    self.raster[y][x] = None
                    self.raster[y+1][x] = quadrat_id
                    self.canvas.move(quadrat_id, 0, (self.feld_größe+1))

    def bewege_links(self):
        if self.kann_bewegen(-1, 0):
            self.aktuelle_position = (self.aktuelle_position[0] - 1, self.aktuelle_position[1])
            for id in self.tetromino_ids:
                self.canvas.move(id, -self.feld_größe - 1, 0)

    def bewege_rechts(self):
        if self.kann_bewegen(1, 0):
            self.aktuelle_position = (self.aktuelle_position[0] + 1, self.aktuelle_position[1])
            for id in self.tetromino_ids:
                self.canvas.move(id, self.feld_größe + 1, 0)

    def bewege_unten(self):
        if self.kann_bewegen(0, 1):
            self.aktuelle_position = (self.aktuelle_position[0], self.aktuelle_position[1] + 1)
            for id in self.tetromino_ids:
                self.canvas.move(id, 0, self.feld_größe + 1)

    def drehe_tetromino(self):
        alte_tetromino = self.aktuelles_tetromino
        neue_tetromino = [(-y, x) for x, y in alte_tetromino]
        if all(self.kann_bewegen(x, y) for x, y in neue_tetromino):
            self.aktuelles_tetromino = neue_tetromino
            for id, (x, y) in zip(self.tetromino_ids, neue_tetromino):
                self.canvas.coords(id, 
                                   (self.aktuelle_position[0] + x) * (self.feld_größe + 1), 
                                   (self.aktuelle_position[1] + y) * (self.feld_größe + 1), 
                                   (self.aktuelle_position[0] + x + 1) * (self.feld_größe + 1), 
                                   (self.aktuelle_position[1] + y + 1) * (self.feld_größe + 1))

# Beispiel Nutzung
root = tk.Tk()
root.title("Tetris")
tetris_gui = TetrisGUI(root, 10, 20, 30)  # Feldgröße erhöht
root.mainloop()
