import os
import sqlite3
from werkzeug.security import generate_password_hash

def build_empty_database():
    db_file = "database.db"
    
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Cleaned old database binary tree node footprint.")

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    try:
        print("🧱 Reading relational schemas...")
        with open("schema.sql", "r", encoding="utf-8") as schema_f:
            cursor.executescript(schema_f.read())

        print("🌱 Seeding relational structural testing accounts...")
        with open("seed.sql", "r", encoding="utf-8") as seed_f:
            cursor.executescript(seed_f.read())

        admin_password = generate_password_hash("admin123",method='pbkdf2')
        cursor.execute(
            "INSERT INTO users (email,first_name,last_name, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            ('admin@gmail.com', 'Admin', 'xxx', admin_password, 'admin')
        )


        connection.commit()
        print("🚀 Database builds evaluated successfully. operational deployment clean.")
    except Exception as failure:
        connection.rollback()
        print(f"❌ Initialization aborted due to SQL execution failure: {failure}")
    finally:
        connection.close()

if __name__ == "__main__":
    build_empty_database()