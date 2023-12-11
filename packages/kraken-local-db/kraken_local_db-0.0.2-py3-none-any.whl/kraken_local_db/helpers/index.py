

import sqlite3
import json
import os



def create_index_if_not_exists(db_path, table_name, index_name, columns):
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