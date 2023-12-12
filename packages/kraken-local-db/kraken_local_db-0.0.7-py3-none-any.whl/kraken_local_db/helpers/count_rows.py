

import sqlite3
import json
import os


def count_rows(db_path, table_name):
    """
    Count the number of rows in a specified table in a SQLite database.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to count rows in.
    :return: The number of rows in the table.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to count the number of rows in the table
    query = f"SELECT COUNT(*) FROM {table_name}"

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch the count result
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the database connection
        conn.close()