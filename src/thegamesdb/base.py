
class ResourceException(Exception):
    pass


class Resource(object):
    """
    """
    name = None
    get_path = None
    list_path = None
    item_class = None

    def __init__(self, db):
        self.db = db

    def _build_item(self, **data):
        return self.item_class(self, **data)

    def get(self, id):
        """
        """
        data = self.db.get_data(self.get_path, id=id)
        return self._build_item(**data)

    def list(self, **kwargs):
        """
        """
        raise NotImplementedError
