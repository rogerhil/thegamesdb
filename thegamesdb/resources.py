# TheGamesDb API, Python Wrapper - http://wiki.thegamesdb.net/index.php/Main_Page
# Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

""" This module contains the resources classes used in the main TheGamesDb
class.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"

from .base import Resource, GamesDbException
from .items import Game, Platform


class GameResource(Resource):
    """ Game resource.
    """
    name = 'Game'
    get_path = 'GetGame.php'
    list_path = 'GetGamesList.php'
    updates_path = 'Updates.php'
    item_class = Game

    def list(self, name, platform='', genre=''):
        """ The name argument is required for this method as per the API
        server specification. This method also provides the platform and genre
        optional arguments as filters.
        """
        data_list = self.db.get_data(self.list_path, name=name,
                                     platform=platform, genre=genre)
        data_list = data_list.get('Data') or {}
        games = data_list.get('Game') or []
        return [self._build_item(**i) for i in games]

    def updates(self, seconds):
        data_list = self.db.get_data(self.updates_path, time=seconds)
        if 'Items' not in data_list:
            raise GamesDbException(data_list.get('Error', str(data_list)))
        return dict(time=data_list['Items']['Time'],
                    games=data_list['Items']['Game'])


class PlatformResource(Resource):
    """ Platform resource.
    """
    name = 'Platform'
    get_path = 'GetPlatform.php'
    list_path = 'GetPlatformsList.php'
    games_path = 'PlatformGames.php'
    item_class = Platform

    def __repr__(self):
        """ This method is overrode to include the "games" method in the object
        representation.
        """
        return "<%s get,list,games>" % self.__class__.__name__

    def list(self):
        """ No argument is required for this method as per the API server
        specification.
        """
        data_list = self.db.get_data(self.list_path)
        data_list = data_list.get('Data') or {}
        platforms = (data_list.get('Platforms') or {}).get('Platform') or []
        return [self._build_item(**i) for i in platforms]

    def games(self, platform):
        """ It returns a list of games given the platform *alias* (usually is
        the game name separated by "-" instead of white spaces).
        """
        platform = platform.lower()
        data_list = self.db.get_data(self.games_path, platform=platform)
        data_list = data_list.get('Data') or {}
        return [Game(self.db.game, **i) for i in data_list.get('Game') or {}]
