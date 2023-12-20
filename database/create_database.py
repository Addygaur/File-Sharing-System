import sqlite3

def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('user.db')
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # SQL query to create the 'users' table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        creation_datetime TEXT,
        is_active BOOLEAN,
        role TEXT
    );
    '''

    # Execute the query to create the table
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Table 'users' created successfully.")

# Check if the script is being run as the main program
if __name__ == '__main__':
    # Call the create_users_table function to create the 'users' table
    create_users_table()
