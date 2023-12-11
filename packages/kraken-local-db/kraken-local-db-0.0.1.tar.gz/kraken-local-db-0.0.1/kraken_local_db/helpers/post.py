
import sqlite3
import json



def post(db_path, table_name, record_type, record_id, json_data, json_column_name='json_data'):
    """
    Store a JSON record in a SQLite database, creating the table if it doesn't exist.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table where the JSON data will be stored.
    :param json_data: The JSON data to store (as a dictionary).
    :param json_column_name: The name of the column to store JSON data.
    """
    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if it does not exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        record_type TEXT,
        record_id TEXT,
        {json_column_name} TEXT
    )
    """
    cursor.execute(create_table_query)

    # SQL query to insert the JSON data
    insert_query = f"INSERT INTO {table_name} ('record_type', 'record_id', {json_column_name}) VALUES (?, ?, ?)"

    try:
        # Execute the insert query
        cursor.execute(insert_query, (record_type, record_id, json_str,))

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Post An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

    return True