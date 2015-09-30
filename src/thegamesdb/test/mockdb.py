import os
from io import StringIO
from urllib.parse import urlencode

from ..api import TheGamesDb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MockException(Exception):
    pass


class TheGamesDbMock(TheGamesDb):

    xml_path = os.path.join(BASE_DIR, 'test/xml')

    def get_response(self, path, **params):
        """
        """
        qs = ("?%s" % urlencode(params) if params else "")
        service = "%s%s" % (path, qs)
        response = None
        for filename in os.listdir(self.xml_path):
            if service == os.path.splitext(filename)[0]:
                with open(os.path.join(self.xml_path, filename)) as xml:
                    response = StringIO(xml.read())
        if response is None:
            raise MockException('No mock xml file for "%s"' % service)
        return response
