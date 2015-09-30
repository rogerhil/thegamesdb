from .item import BaseItem


class Game(BaseItem):
    extra_attributes = [
        'overview', 'esrb', 'genres', 'youtube', 'publisher', 'developer',
        'rating', 'similar', 'images'
    ]
    translate = {'gametitle': 'name'}


class Platform(BaseItem):
    extra_attributes = [
        'console', 'controller', 'overview', 'developer', 'manufacturer',
        'cpu', 'memory', 'graphics', 'sound', 'display', 'media',
        'maxcontrollers', 'rating', 'Images'
    ]
    translate = {'platform': 'name'}

    def games(self):
        return self.resource.games(self.name)
