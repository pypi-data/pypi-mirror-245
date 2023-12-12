import os
import pathlib
from kraken_local_db.helpers import get, post, search, init_db, count_rows, delete

class Kraken_local_db:
    """Class to manage local sqlite database

    Attributes:
    - db_path: The filepath of the database file
    - len(): number of records in table

    Methods:
    - get(record_type, record_id):
        Get a single record
    - search(key, value):
        Search database base don key, value. Supports dot notation
    - post(records):
        Post one or many record to database
    - delete(record_type, record_id):
        delete a single record
    - drop:
        deletes database file
        
    """


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


    def delete(self, record_type, record_id):
        """delete record
        """
        return delete.delete(self._db_path, self._table, record_type, record_id)

    def drop(self):
        """Remove database file
        """
        # Clean up
        file_to_rem = pathlib.Path(self._db_path)
        return file_to_rem.unlink(missing_ok = True)
        