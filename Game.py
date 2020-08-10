import pgzrun

import GameObjects as go

WIDTH = 1200
HEIGHT = 900


class ActorMaker:

    def make_actor(self, img_name):
        return Actor(img_name)


actor_maker = ActorMaker()
world = go.World(actor_maker, WIDTH, HEIGHT)

space_ship = world.make_game_actor("space_ship_005")
center_x, center_y = world.get_center()
space_ship.set_location(center_x, HEIGHT - 50)
meteor = world.make_game_actor("space_meteor_001_40p")
world.add_actor(space_ship)
world.add_actor(meteor)

ship_mover = go.CanMoveLeftRight(space_ship, keys.LEFT, keys.RIGHT)
can_fire = go.CanFire(space_ship,  keys.SPACE)
world.add_key_handler(ship_mover)
world.add_key_handler(can_fire)

meteor_updater = go.UpDownPath(meteor, 300, 0, True)
world.add_location_updater(meteor_updater)


def draw():
    screen.clear()
    world.draw()


def update():
    world.update()


def on_key_down(key, mod):
    world.on_key_down(key, mod)


pgzrun.go()
