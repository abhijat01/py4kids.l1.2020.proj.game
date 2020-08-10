import pgzrun

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
space_ship_actor = go.GameActor(space_ship, world=world)
meteor = actor_maker.make_actor("space_meteor_001_40p")
meteor_actor = go.GameActor(meteor, world=world)

world.add_actor(space_ship_actor)
world.add_actor(meteor_actor)
meteor_updater = go.UpDownPath(meteor_actor, 300, 0, coming_down=True)
world.add_updater(meteor_updater)

def draw():
    screen.clear()
    world.draw()


def update():
    world.update()


def on_key_down(key, mod):
    pass


pgzrun.go()
