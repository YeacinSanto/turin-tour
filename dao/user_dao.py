from dao.db import get_db_connection
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_by_id(user_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return None
    langs = row['languages'].split(',') if row['languages'] else []
    return User(row['id'], row['email'], row['first_name'], row['last_name'], row['role'], langs)

def verify_user(email,password):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    conn.close()
    
    if row and check_password_hash(row['password_hash'],password):
        langs = row['languages'].split(',') if row['languages'] else []
        
        return User(row['id'],row['email'],row['first_name'], row['last_name'], row['role'], langs)
    return None