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

""" This module contains the base item class to represent an item of the API.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"


class LazyItemValue(object):
    """ Just to represent a value for an attribute of the BaseItem to fetch
    data only when is necessary.
    """


class BaseItem(object):
    """ This class is to represent an item of the API. The following attributes
    may be provided in the children classes:
     - extra_attributes: usually the api doesn't fetch the entire the data
                         related to an item, so we determine which are the
                         remaining attributes to be fetched lately once
                         the attribute is triggered.
     - translate: some attributes in the api are not consistent along different
                  service data, so use this dict to translate attributes coming
                  from api to consistent ones.
    """
    extra_attributes = []
    translate = {}
    aliases_fix = {}

    def __init__(self, resource, **kwargs):
        """ It requires the correspond resource instance and generic kwargs
        to set this item attributes. The "extra_attibutes" are being set as
        a LazyItemValue() instance firstly. Afterwards, the __getattribute__
        method may lately return the proper value coming from the API.
        The "alias" attribute are not always present, so is saves as a cache
        value _alias in case is present, otherwise keep it as None. The "alias"
        property in this class provides the value properly.
        """
        self.resource = resource
        self._extra_data = {}
        self.name = None
        self._alias = None
        for key in self.extra_attributes:
            setattr(self, key.lower(), LazyItemValue())
        for key, value in kwargs.items():
            attr = key.lower()
            if attr == 'alias':
                setattr(self, '_alias', value)
                continue
            if attr in self.translate:
                attr = self.translate[attr]
            setattr(self, attr, value)

    def __str__(self):
        """ Just the item name.
        """
        return str(self.name)

    def __repr__(self):
        """ The object representation.
        """
        return "<%s: %s>" % (self.__class__.__name__, str(self))

    def __getattribute__(self, item):
        """ It checks for LazyItemValue value to get the value properly because
        the information got from the API server was incomplete, (usually
        because list services only provides a few necessary data, more
        complete data must be taken from "get" services).
        """
        value = super(BaseItem, self).__getattribute__(item)
        if isinstance(value, LazyItemValue):
            d = super(BaseItem, self).__getattribute__('__dict__')
            resource = d['resource']
            data = resource.db.get_data(resource.get_path, id=d['id'])
            for key, value in data['Data'][resource.name].items():
                setattr(self, key.lower(), value)
        value = super(BaseItem, self).__getattribute__(item)
        if isinstance(value, LazyItemValue):
            setattr(self, item, None)
        return super(BaseItem, self).__getattribute__(item)

    @property
    def alias(self):
        """ If the _alias cache is None, just build the alias from the item
        name.
        """
        if self._alias is None:
            if self.name in self.aliases_fix:
                self._alias = self.aliases_fix[self.name]
            else:
                self._alias = self.name.lower()\
                                  .replace(' ', '-')\
                                  .replace('(', '')\
                                  .replace(')', '')
        return self._alias
