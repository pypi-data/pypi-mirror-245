

import sqlite3
import json
import os



def init_db(db_path, table_name, json_column_name):
    """
    """
    _create_db_if_not_exists(db_path, table_name, json_column_name)
    
    _create_index_if_not_exists(db_path, table_name, 'index_record_type', ['record_type'])

    _create_index_if_not_exists(db_path, table_name, 'index_record_id', ['record_id'])

    _create_index_if_not_exists(db_path, table_name, 'index_type_id', ['record_type', 'record_id'])
    
    



def _create_db_if_not_exists(db_path, table_name, json_column_name):
    """
    Retrieve a record from a SQLite database based on record_type and record_id.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to search in.
    :param record_type: The value of the 'record_type' field to match.
    :param record_id: The value of the 'record_id' field to match.
    :return: A tuple representing the matching record, or None if no match is found.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if it does not exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        record_type TEXT,
        record_id TEXT,
        json_data TEXT,
        UNIQUE(record_type, record_id)
    )
    """
    cursor.execute(create_table_query)
    return




def _create_index_if_not_exists(db_path, table_name, index_name, columns):
    """
    Create an index on a SQLite table if it doesn't already exist.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table on which the index is to be created.
    :param index_name: Name of the index to create.
    :param columns: A list of column names to include in the index.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Format the column names for the SQL statement
    columns_str = ", ".join(columns)

    # SQL query to create the index if it does not exist
    query = f"""
    CREATE INDEX IF NOT EXISTS {index_name}
    ON {table_name} ({columns_str})
    """

    try:
        # Execute the query
        cursor.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()