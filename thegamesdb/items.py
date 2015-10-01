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

""" Define the classes to represent the items returned from this api.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"

from .item import BaseItem


class Game(BaseItem):
    """ The Game item must translate "gametitle" coming from the XML to "name"
    to keep consistency/
    """
    extra_attributes = [
        'platform', 'overview', 'esrb', 'genres', 'players', 'co-op',
        'youtube', 'publisher', 'developer', 'rating', 'similar', 'images'
    ]
    translate = {'gametitle': 'name', 'co-op': 'co_op'}

    def __str__(self):
        """ Overrides to include the platform.
        """
        return "%s (%s)" % (str(self.name), self.platform)


class Platform(BaseItem):
    """ The Platform item must translate "platform" attribute coming from the
    XML to "name" to keep consistency.
    """
    extra_attributes = [
        'console', 'controller', 'overview', 'developer', 'manufacturer',
        'cpu', 'memory', 'graphics', 'sound', 'display', 'media',
        'maxcontrollers', 'rating', 'images'
    ]
    translate = {'platform': 'name'}
    aliases_fix = {
        'Nintendo Game Boy': 'nintendo-gameboy',
        'Nintendo Game Boy Advance': 'nintendo-gameboy-advance',
        'Nintendo Game Boy Color': 'nintendo-gameboy-color',
    }

    def games(self):
        """ This resource provides this extra method to retrieve all the games
        for this platform.
        """
        return self.resource.games(self.name)
