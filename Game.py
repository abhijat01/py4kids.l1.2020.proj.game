import pgzrun

import GameObjects as go

WIDTH = 1200
HEIGHT = 900


class ActorMaker:

    def make_actor(self, img_name):
        return Actor(img_name)

actor_maker = ActorMaker()
actor = actor_maker.make_actor("space_ship_005")
actor.center = WIDTH/2, HEIGHT -50
meteor = actor_maker.make_actor("space_meteor_001_40p")

def draw():
    screen.clear()
    actor.draw()
    meteor.draw()


def update():
    pass


def on_key_down(key, mod):
    pass


pgzrun.go()
