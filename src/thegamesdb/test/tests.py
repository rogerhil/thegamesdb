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
""" Tests implementation.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"

from unittest import TestCase

from .mockdb import TheGamesDbMock
from ..items import Game, Platform


class BaseTest(TestCase):

    def setUp(self):
        self.api = TheGamesDbMock()


class TestGame(BaseTest):

    def test_list(self):
        games = self.api.game.list("Origins")
        for game in games:
            self._test_individual_game(game)

    def test_get(self):
        game = self.api.game.get(49)
        self._test_individual_game(game)
        game = self.api.game.get(4209)
        self._test_individual_game(game)

    def _test_individual_game(self, game):
        self.assertTrue(isinstance(game, Game))
        self.assertFalse(getattr(game, 'id', None) is None)
        self.assertFalse(getattr(game, 'name', None) is None)
        self.assertFalse(getattr(game, 'releasedate', None) is None)
        self.assertFalse(getattr(game, 'platform', None) is None)
        for attr in Game.extra_attributes:
            self.assertTrue(hasattr(game, attr))
            self.assertFalse(getattr(game, attr) is None)


class TestPlatform(BaseTest):

    def test_list(self):
        platforms = self.api.platfomr.list()
        for platform in platforms:
            self._test_individual_game(platform)

    def test_get(self):
        platform = self.api.platform.get(15)
        self._test_individual_platform(platform)

    def _test_individual_platform(self, platform):
        self.assertTrue(isinstance(platform, Platform))
        self.assertFalse(getattr(platform, 'id', None) is None)
        self.assertFalse(getattr(platform, 'name', None) is None)
        self.assertFalse(getattr(platform, 'alias', None) is None)
        for attr in Platform.extra_attributes:
            self.assertTrue(hasattr(platform, attr))
            self.assertFalse(getattr(platform, attr) is None)

    def test_aliases(self):
        platforms = self.api.platfomr.list()
        for platform in platforms:
            platform_from_get = self.api.platform.get(platform.id)
            self.assertEquals(platform.alias, platform_from_get.alias)
