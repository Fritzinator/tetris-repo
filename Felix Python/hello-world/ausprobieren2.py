import tkinter as tk

class KoordinatenRasterGUI:
    def __init__(self, master, breite, höhe, feld_größe):
        self.master = master
        self.breite = breite
        self.höhe = höhe
        self.feld_größe = feld_größe
        self.raster = [[None for _ in range(breite)] for _ in range(höhe)]

        self.canvas = tk.Canvas(master, width=breite*(feld_größe+1), height=höhe*(feld_größe+1))
        self.canvas.pack()

        for i in range(1, breite):
            self.canvas.create_line(i*(feld_größe+1), 0, i*(feld_größe+1), höhe*(feld_größe+1), fill="black")
        for j in range(1, höhe):
            self.canvas.create_line(0, j*(feld_größe+1), breite*(feld_größe+1), j*(feld_größe+1), fill="black")

        self.canvas.bind("<Button-1>", self.feld_anwählen)

    def feld_anwählen(self, event):
        x = event.x // (self.feld_größe+1)
        y = event.y // (self.feld_größe+1)

        if 0 <= x < self.breite and 0 <= y < self.höhe:
            if self.raster[y][x] is None:
                self.raster[y][x] = self.canvas.create_rectangle(x*(self.feld_größe+1), y*(self.feld_größe+1), (x+1)*(self.feld_größe+1), (y+1)*(self.feld_größe+1), fill="red")
                print(f"Das Feld bei ({x}, {y}) wurde ausgewählt und ist jetzt rot.")
            else:
                self.canvas.delete(self.raster[y][x])
                self.raster[y][x] = None
                print(f"Das Feld bei ({x}, {y}) wurde freigegeben.")

# Beispiel Nutzung
root = tk.Tk()
root.title("Koordinatenraster")
raster_gui = KoordinatenRasterGUI(root, 10, 10, 40)
root.mainloop()
