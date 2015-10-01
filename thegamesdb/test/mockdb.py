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
""" This module contains the an implementation of the main class TheGamesDb
mocked, for testing purposes, to read XML files instead of requesting URLs.
"""

__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"

import os
from urllib.parse import urlencode

from ..api import TheGamesDb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MockException(Exception):
    pass


class TheGamesDbMock(TheGamesDb):
    """ It inherits from TheGamesDb to especially overrides the get_response
    method to read XML files saved locally instead of using the network.
    """

    def __init__(self, xml_path=None):
        """ Overrides just to include the options argument xml_path.
        """
        super(TheGamesDbMock, self).__init__()
        self.xml_path = XmlsDb.xml_path if xml_path is None else xml_path

    def get_response(self, path, **params):
        """ Each XML file save has the exact service path name with the
        parameters, so it's easy to get the proper by checking the file names.
        If the the service path + query string doesn't match any XML file, it
        raises the MockException.
        """
        service = XmlsDb.get_service_path_by_path_params(path, **params)
        response = None
        for filename in os.listdir(self.xml_path):
            if service == os.path.splitext(filename)[0]:
                with open(os.path.join(self.xml_path, filename)) as xml:
                    response = xml.read()
        if response is None:
            raise MockException('No mock xml file for "%s"' % service)
        return response


class XmlsDb(object):

    xml_path = os.path.join(BASE_DIR, 'test/xml')

    def __init__(self):
        self.api = TheGamesDb()

    @staticmethod
    def get_service_path_by_path_params(path, **params):
        params = dict([(k, v) for k, v in params.items() if v])
        qs = ("?%s" % urlencode(params) if params else "")
        service = "%s%s" % (path, qs)
        return service

    @classmethod
    def save_xml(cls, data, path, **params):
        service = cls.get_service_path_by_path_params(path, **params)
        with open(os.path.join(cls.xml_path, "%s.xml" % service), 'w') as xml:
            xml.write(data.decode('utf-8'))

    def update_platforms_xmls(self):
        platforms = self.api.platform.list()
        self.save_xml(self.api.last_response, self.api.platform.list_path)
        for platform in platforms:
            self.api.platform.get(platform.id)
            platform_name_plus = platform.name.lower()
            self.save_xml(self.api.last_response, self.api.platform.get_path,
                          id=platform.id)
            platform.games()
            self.save_xml(self.api.last_response, self.api.platform.games_path,
                          platform=platform_name_plus)

    def update_games_xmls(self):
        games = self.api.game.list(name='x-men')
        self.save_xml(self.api.last_response, self.api.game.list_path,
                      name='x-men')
        for game in games:
            self.api.game.get(game.id)
            self.save_xml(self.api.last_response, self.api.game.get_path,
                          id=game.id)
        games = self.api.game.list(name='Origins')
        self.save_xml(self.api.last_response, self.api.game.list_path,
                      name='Origins')
        for game in games:
            self.api.game.get(game.id)
            self.save_xml(self.api.last_response, self.api.game.get_path,
                          id=game.id)

