

class GameActor:
    def __init__(self, actor, world):
        self.actor = actor
        self.my_world = world

    def set_location(self, x, y):
        self.actor.center = (x, y)

    def move_by(self, del_x, del_y):
        x, y = self.actor.center
        self.actor.center = x + del_x, y + del_y

    def draw(self):
        self.actor.draw()

    def update(self):
        pass

    def world(self):
        return self.my_world

    def center(self):
        return self.actor.center


class LocationUpdater:
    def __init__(self, ican_move,start_x, start_y):
        self.ican_move = ican_move
        self.start_x = start_x
        self.start_y = start_y
        self.speed = 1.0
        self.x = start_x
        self.y = start_y
        ican_move.set_location(start_x, start_y)

    def update(self):
        x,y = self.next_x(), self.next_y()
        self.ican_move.set_location(x,y)

    def next_x(self):
        self.x

    def next_y(self):
        self.y


class World:

    def __init__(self, actor_maker, w, h):
        self.w = w
        self.h = h
        self.actor_maker = actor_maker
        self.actors = []
        self.key_handlers = []
        self.location_updater = []

    def make_pg0_actor(self, img_name):
        act = self.actor_maker.make_actor(img_name)
        return act

    def get_center(self):
        return self.w/2, self.h/2

    def add_actor(self, game_actor):
        self.actors.append(game_actor)

    def add_location_updater(self, updater):
        self.location_updater.append(updater)

    def add_key_handler(self, key_handler):
        self.key_handlers.append(key_handler)

    def remove_location_updater(self, updater):
        self.location_updater.remove(updater)

    def remove_actor(self, game_actor):
        self.actors.remove(game_actor)

    def remove_key_handler(self, key_handler):
        self.key_handlers.remove(key_handler)

    def on_key_down(self, key, mod):
        for handler in self.key_handlers:
            handler.on_key_down(key, mod)

    def draw(self):
        for actor in self.actors:
            actor.draw()

    def update(self):
        for updater in self.location_updater:
            updater.update()


class UpDownPath(LocationUpdater):

    def __init__(self, ican_move, start_x, start_y, coming_down):
        super().__init__(ican_move, start_x, start_y)
        if coming_down:
            self.del_y = 5
        else:
            self.del_y = -5

    def next_x(self):
        return self.x

    def next_y(self):
        self.y = self.y+self.del_y
        world = self.ican_move.world()
        if self.y > world.h + 400:
            self.y = self.start_y

        if self.y < -400:
            self.y = self.start_y

        return self.y


class Ship(GameActor):
    def __init__(self, actor, world, left_key, right_key, fire_key):
        super().__init__(actor, world)
        self.left_key = left_key
        self.right_key = right_key
        self.fire_key = fire_key

    def on_key_down(self, key, mod):
        if key == self.left_key:
            self.move_by(-5,0)
        if key == self.right_key:
            self.move_by(5,0)
        if key == self.fire_key:
            self.fire()

    def fire(self):
        world = self.my_world
        missile_act = world.make_pg0_actor("space_missile_009")
        missile = GameActor(missile_act, world)
        x,y = self.center()
        y -=40
        go_up = UpDownPath(missile, x,y, False )
        world.add_actor(missile)
        world.add_location_updater(go_up)

