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

""" This is the base module that contains the base abstract class for a generic
game resource.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"


class GamesDbException(Exception):
    pass


class Resource(object):
    """ Abstract class for a generic game resource. Child classes must provide
    the following attributes:
     - name: the resource name based on the XML tag,
             e.g.: <Platform></Platform> => Platform.
     - get_path: the path to get an item,, e.g.: GetGame.php
     - list_path: the path to list items,, e.g.: GetGamesList.php
     - item_class: a class that represents and item for this resource.
    """
    name = None
    get_path = None
    list_path = None
    item_class = None

    def __init__(self, db):
        """ It requires the main TheGamesDb object.
        """
        self.db = db

    def __str__(self):
        """ Just this resource name.
        """
        return str(self.name)

    def __repr__(self):
        """ The object string representation includes the important methods of
        this resource.
        """
        return "<%s get,list>" % self.__class__.__name__

    def _build_item(self, **data):
        """ Instantiate an item using the item_class defined in the class
        passing this resource as the first argument and the correspond data.
        """
        return self.item_class(self, **data)

    def get(self, id):
        """ Gets the dict data and builds the item object.
        """
        data = self.db.get_data(self.get_path, id=id)
        return self._build_item(**data['Data'][self.name])

    def list(self, **kwargs):
        """ This method is abstract and needs to be implemented because the
        kwargs might be different per resource.
        """
        raise NotImplementedError
