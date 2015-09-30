from .base import Resource
from .items import Game, Platform


class GameResource(Resource):
    name = 'game'
    get_path = 'GetGame.php'
    list_path = 'GetGamesList.php'
    item_class = Game

    def list(self, name, platform='', genre=''):
        return super(GameResource, self).list(name=name, platform=platform,
                                              genre=genre)


class PlatformResource(Resource):
    name = 'platform'
    get_path = 'GetPlatform.php'
    list_path = 'GetPlatformsList.php'
    item_class = Platform

    def get(self, id):
        data = self.db.get_data(self.get_path, id=id)
        return self._build_item(**data['Data']['Platform'])

    def list(self):
        data_list = self.db.get_data(self.list_path)
        platforms = data_list['Data']['Platforms']['Platform']
        return [self._build_item(**i) for i in platforms]

    def games(self, platform):
        platform = platform.replace('-', ' ')
        data_list = self.db.get_data('PlatformGames.php', platform=platform)
        return [Game(self.db.game, **i) for i in data_list['Data']['Game']]
