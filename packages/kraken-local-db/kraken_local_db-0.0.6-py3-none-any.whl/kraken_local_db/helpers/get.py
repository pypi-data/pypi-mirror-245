

import sqlite3
import json


def get(db_path, table_name, record_type='%', record_id='%'):
    """
    Retrieve a record from a SQLite database based on record_type and record_id.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to search in.
    :param record_type: The value of the 'record_type' field to match.
    :param record_id: The value of the 'record_id' field to match.
    :return: A tuple representing the matching record, or None if no match is found.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to select the record based on record_type and record_id
    query = f"""
    SELECT * FROM {table_name}
    WHERE record_type = ? AND record_id = ?
    """

    try:
        # Execute the query
        cursor.execute(query, (record_type, record_id))

        # Fetch the first matching record
        result = cursor.fetchone()
        if not result:
            return None
        
        record_type, record_id, content = result
        record = json.loads(content)
        
        return record
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the database connection
        conn.close()


