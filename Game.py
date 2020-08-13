import pgzrun

import random

import GameObjects as go

WIDTH = 1200
HEIGHT = 900


class ActorMaker:

    def make_actor(self, img_name):
        return Actor(img_name)

actor_maker = ActorMaker()
world = go.World(actor_maker, WIDTH, HEIGHT)
space_ship = actor_maker.make_actor("space_ship_005")
space_ship.center = WIDTH / 2, HEIGHT - 50
space_ship_actor = go.Ship(space_ship, world=world,
                           left_key=keys.LEFT,
                           right_key=keys.RIGHT,
                           fire_key=keys.SPACE)

for i in range(8):
    x = random.randint(10,1150)
    y = random.randint(10,850)
    world.add_meteor( x,y)

world.add_actor(space_ship_actor)
world.add_key_listener(space_ship_actor)



def draw():
    screen.clear()
    world.draw()


def update():
    world.update()


def on_key_down(key, mod):
    world.on_key_down(key, mod)


pgzrun.go()
