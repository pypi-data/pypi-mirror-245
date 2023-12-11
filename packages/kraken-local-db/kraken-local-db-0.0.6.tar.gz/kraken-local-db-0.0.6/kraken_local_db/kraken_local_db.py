import os

from kraken_local_db.helpers import get, post, search, init_db, count_rows

class Kraken_local_db:


    def __init__(self, path=None):

        self._db_path = None
        self._table = 'things'
        self._json_field = 'json_data'

        if path:
            self.db_path = path
        else:
            self._db_path = 'data/things.db'
            

        self.init_db()

    def __len__(self):
        return count_rows.count_rows(self._db_path, self._table)
    
    def init_db(self):
        """
        """
        return init_db.init_db(self._db_path, self._table, self._json_field)

    
    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, value):
        self._db_path = value
        

    def get(self, record_type, record_id):
        """Retrieve a specific record
        """
        return get.get(self._db_path, self._table, record_type, record_id)


    def search(self, key, value):
        """Search records
        """
        return search.search(self._db_path, self._table, self._json_field, key, value)

    
    def post(self, record):
        """Post a record
        """
    
        return post.post(self._db_path, self._table, record, self._json_field)
        