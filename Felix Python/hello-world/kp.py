import tkinter as tk
import random

class TetrisGUI:
    def __init__(self, master, breite, höhe, feld_größe):
        self.master = master
        self.breite = breite
        self.höhe = höhe
        self.feld_größe = feld_größe
        self.raster = [[None for _ in range(breite)] for _ in range(höhe)]
        self.aktuelles_tetromino = None
        self.aktuelle_position = None
        self.spiel_läuft = True
        self.punkte = 0
        self.highscore = 0

        self.canvas = tk.Canvas(master, width=breite*(feld_größe+1), height=höhe*(feld_größe+1))
        self.canvas.pack()

        self.highscore_label = tk.Label(master, text=f"Highscore: {self.highscore}", font=("Helvetica", 12))
        self.highscore_label.pack()

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
        x = random.randint(0, self.breite - 1)
        y = 1  # Startposition in der zweitobersten Reihe
        if self.raster[y][x] is None:
            self.aktuelles_tetromino = self.erstelle_tetromino(x, y)
            self.aktuelle_position = (x, y)
        else:
            self.spiel_ende()
            return

        self.bewege_tetromino()

    def erstelle_tetromino(self, x, y):
        farben = ["cyan", "yellow", "green", "purple", "orange", "blue", "red"]
        farbe = random.choice(farben)
        tetromino_id = []
        if farbe == "cyan":  # I-Tetromino
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, y*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+2)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+3)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+3)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+4)*self.feld_größe,
                                                             fill=farbe))
        elif farbe == "yellow":  # O-Tetromino
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, y*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, y*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
        elif farbe == "green":  # S-Tetromino
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, y*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+2)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+3)*self.feld_größe,
                                                             fill=farbe))
        elif farbe == "purple":  # T-Tetromino
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, y*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, y*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+2)*self.feld_größe, y*self.feld_größe,
                                                             (x+3)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
        elif farbe == "orange":  # L-Tetromino
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, y*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+2)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+3)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, (y+2)*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+3)*self.feld_größe,
                                                             fill=farbe))
        elif farbe == "blue":  # J-Tetromino
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, y*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle((x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             (x+2)*self.feld_größe, (y+2)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, (y+2)*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+3)*self.feld_größe,
                                                             fill=farbe))
            tetromino_id.append(self.canvas.create_rectangle(x*self.feld_größe, y*self.feld_größe,
                                                             (x+1)*self.feld_größe, (y+1)*self.feld_größe,
                                                             fill=farbe))
       
