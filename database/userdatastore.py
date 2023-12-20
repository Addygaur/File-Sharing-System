import sqlite3
from entity.user import user_info
from utils.password_hasher import get_hashed_password


class UserDataStore:

    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = self.dict_factory
        self.cursor = self.conn.cursor()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_user(self, payload: user_info):
        json_data = payload.to_json()
        json_data['password'] = get_hashed_password(json_data['password'])

        try:
            # Define the SQL query to insert data into the 'users' table
            insert_query = '''
            INSERT INTO users (user_id, first_name, last_name, email, password, creation_datetime, is_active, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            '''

            # Extract values from the JSON object
            values = (
                json_data["user_id"],
                json_data["first_name"],
                json_data["last_name"],
                json_data["email"],
                json_data["password"],
                json_data["creation_datetime"],
                json_data["is_active"],
                json_data["role"]
            )

            # Execute the SQL query
            self.cursor.execute(insert_query, values)

            # Commit the changes
            self.conn.commit()

            print("Data inserted successfully.")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def check_email_id(self, email_id):
        try:
            select_all_query = f"SELECT * FROM users WHERE email = '{email_id}';"

            self.cursor.execute(select_all_query)

            # Fetch all rows from the result set
            rows = self.cursor.fetchall()
            if rows:
                return rows[0]
            else:
                return False
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
