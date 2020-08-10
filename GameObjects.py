class GameActor:

    def __init__(self, actor, world):
        self.actor = actor
        self.my_world = world

    def set_location(self, x, y):
        self.actor.center = x,y

    def move_by(self, del_x, del_y):
        x, y =  self.actor.center
        self.actor.center = x+del_x, y+del_y

    def world(self):
        return self.my_world

    def draw(self):
        self.actor.draw()


class World:
    def __init__(self, actor_maker, w, h ):
        self.w = w
        self.h = h
        self.actor_maker = actor_maker
        self.actors = []
        self.updaters = []

    def add_updater(self, updater):
        self.updaters.append(updater)

    def remove_updater(self, updater):
        self.updaters.remove(updater)

    def draw(self):
        for actor in self.actors:
            actor.draw()

    def update(self):
        for updater in self.updaters:
            updater.update()

    def add_actor(self, actor):
        self.actors.append(actor)

    def remove_actor(self, actor):
        self.actors.remove(actor)


class LocationUpdater:
    def __init__(self, game_actor, start_x, start_y):
        self.game_actor = game_actor
        self.start_x = start_x
        self.start_y = start_y
        self.speed = 1.0
        self.x = start_x
        self.y = start_y

    def update(self):
        x,y = self.next_x(), self.next_y()
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
        if self.y > (h + 100) :
            self.y = -100

        return self.y


