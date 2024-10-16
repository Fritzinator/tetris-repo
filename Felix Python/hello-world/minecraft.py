from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
Sky()

def add_box(position):
    Button(
        parent=scene,
        model='cube',
        origin=0.5,
        color=color.blue,
        position=position 
    )

add_box( (0, 0, 0) )

add_box(0,0,0)

app.run()
