class GameActor:

    def __init__(self, actor, world):
        self.actor = actor
        self.my_world = world
        self.location_updater = None

    def set_location(self, x, y):
        self.actor.center = x, y

    def move_by(self, del_x, del_y):
        x, y = self.actor.center
        self.actor.center = x + del_x, y + del_y

    def world(self):
        return self.my_world

    def draw(self):
        self.actor.draw()

    def set_location_updater(self, location_updater):
        self.location_updater = location_updater

    def remove_from_world(self):
        self.my_world.remove_actor(self)
        self.my_world.remove_updater(self.location_updater)


class World:
    def __init__(self, actor_maker, w, h):
        self.w = w
        self.h = h
        self.actor_maker = actor_maker
        self.actors = []
        self.updaters = []
        self.key_listeners = []

    def add_key_listener(self, key_listener):
        self.key_listeners.append(key_listener)

    def remove_key_listener(self, key_listener):
        self.key_listeners.remove(key_listener)

    def on_key_down(self, key, mod):
        for key_listener in self.key_listeners:
            key_listener.on_key_down(key, mod)

    def add_updater(self, updater):
        self.updaters.append(updater)

    def remove_updater(self, updater):
        self.updaters.remove(updater)

    def get_actor_maker(self):
        return self.actor_maker

    def draw(self):
        for actor in self.actors:
            actor.draw()

    def update(self):
        for updater in self.updaters:
            updater.update()

    def add_actor(self, actor):
        self.actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def add_meteor(self, x, y):
        meteor = self.actor_maker.make_actor("space_meteor_001_40p")
        meteor_actor = GameActor(meteor, world=self)
        self.add_actor(meteor_actor)
        meteor_updater = UpDownPath(meteor_actor, x, y, coming_down=True)
        self.add_updater(meteor_updater)


class LocationUpdater:
    def __init__(self, game_actor, start_x, start_y):
        self.game_actor = game_actor
        self.game_actor.set_location_updater(self)
        self.start_x = start_x
        self.start_y = start_y
        self.speed = 1.0
        self.x = start_x
        self.y = start_y

    def update(self):
        x, y = self.next_x(), self.next_y()
        self.game_actor.set_location(x, y)

    def next_x(self):
        pass

    def next_y(self):
        pass


class UpDownPath(LocationUpdater):
    def __init__(self, game_actor, start_x, start_y, coming_down):
        super().__init__(game_actor, start_x, start_y)
        self.coming_down = coming_down

        if self.coming_down:
            self.del_y = 5
        else:
            self.del_y = -5

    def next_x(self):
        return self.x

    def next_y(self):
        self.y += self.del_y
        world = self.game_actor.world()
        h = world.h
        if self.y > (h + 100):
            self.y = -100

        return self.y


class Ship(GameActor):
    def __init__(self, actor, world, left_key, right_key, fire_key):
        super().__init__(actor, world)
        self.left_key = left_key
        self.right_key = right_key
        self.fire_key = fire_key

    def on_key_down(self, key, mod):
        if key == self.left_key:
            self.move_by(-5, 0)
        if key == self.right_key:
            self.move_by(5, 0)
        if key == self.fire_key:
            self.fire()

    def fire(self):
        actor_maker = self.my_world.get_actor_maker()
        missile = actor_maker.make_actor("space_missile_009")
        missile_actor = Missile(missile, self.my_world)
        self.my_world.add_actor(missile_actor)
        x, y = self.actor.center
        path = UpDownPath(missile_actor, x, y, coming_down=False)
        self.my_world.add_updater(path)


class Missile(GameActor):

    def __init__(self, actor, world):
        super().__init__(actor, world)
        self.am_removed = False

    def set_location(self, x, y):
        self.actor.center = x, y
        print("location now:({},{})".format(x, y))
        world = self.my_world
        w, h = world.w, world.h
        if (x < -10) or (x > (w + 100)) or (y < -10) or (y > (h + 100)):
            self.remove_from_world()

