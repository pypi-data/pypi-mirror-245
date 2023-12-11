
import sqlite3
import json




def search(db_path, table_name, json_field, search_key, search_value):
    """
    Search for records in a SQLite database where a specified JSON field 
    contains a key-value pair.

    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to search in.
    :param json_field: Name of the column containing JSON data.
    :param search_key: The key in the JSON to search for.
    :param search_value: The value associated with the key to search for.
    :return: List of records that match the search criteria.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to find records where the JSON field contains the key-value pair
    query = f"""
    SELECT *
    FROM {table_name}
    WHERE json_extract(json_data, '$.{search_key}') like ?
    """

    # Execute the query and fetch the results
    cursor.execute(query, (search_value,))
    results = cursor.fetchall()
    
    # Close the database connection
    conn.close()

    records = []
    for record_type, record_id, content in results:
        record = json.loads(content)
        records.append(record)
        
    return records
