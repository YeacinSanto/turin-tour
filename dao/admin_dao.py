from dao.db import get_db_connection

def get_admin_dashboard_stats():
    conn = get_db_connection()
    stats = {
        'total_tours': conn.execute("SELECT COUNT(*) FROM tours").fetchone()[0],
        'total_reservations': conn.execute("SELECT COUNT(*) FROM reservations").fetchone()[0],
        'pending_reports': conn.execute("SELECT COUNT(*) FROM tour_reports WHERE report_image IS NULL").fetchone()[0],
        'total_guides': conn.execute("SELECT COUNT(*) FROM users WHERE role = 'guide'").fetchone()[0],
        'total_participants': conn.execute("SELECT COUNT(*) FROM users WHERE role = 'participant'").fetchone()[0]
    }
    conn.close()
    return stats

def get_all_reservations_details(language=None):
    conn = get_db_connection()
    query = """
        SELECT r.tour_date, u.first_name || ' ' || u.last_name as participant_name, t.title as tour_title ,t.language
        FROM reservations r
        JOIN users u ON r.participant_id = u.id
        JOIN tours t ON r.tour_id = t.id
    """
    params = ()
    if language:
        query += " WHERE t.language = ?"
        params = (language,)
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_tours_summary():
    conn = get_db_connection()
    tours = conn.execute("""
        SELECT t.id, t.title, u.first_name || ' ' || u.last_name as guide_name
        FROM tours t
        JOIN users u ON t.guide_id = u.id
    """).fetchall()
    conn.close()
    return [dict(t) for t in tours]


def delete_tour_byId(tour_id):
    conn = get_db_connection()
    # Using the CASCADE delete logic as defined in your initial schema
    conn.execute("DELETE FROM tours WHERE id = ?", (tour_id,))
    conn.commit()
    conn.close()
    
def update_tour_by_admin(tour_id, title, meeting_point, duration, language, max_p, description):
    conn = get_db_connection()
    conn.execute("""
        UPDATE tours 
        SET title = ?, meeting_point = ?, duration = ?, language = ?, max_participants = ?, description = ?
        WHERE id = ?
    """, (title, meeting_point, duration, language, max_p, description, tour_id))
    conn.commit()
    conn.close()
    

def get_host_language_by_tour(tour_id):
    conn = get_db_connection()
    # Assuming your tours table has a 'guide_id' (or 'host_id') 
    # that links to the 'users' table
    row = conn.execute("""
        SELECT u.languages 
        FROM users u
        JOIN tours t ON u.id = t.guide_id 
        WHERE t.id = ?
    """, (tour_id,)).fetchone()
    conn.close()
    return row['languages'] if row else None

def get_report(tour_id):
    conn = get_db_connection()
    conn.execute("""
                 SELECT * FROM tour_reports WHERE id = ?
                 """,tour_id)
    conn.commit()
    conn.close()
    
    
def update_admin_profile(user_id, first_name, last_name):
    conn = get_db_connection()
    conn.execute("""
        UPDATE users
        SET first_name = ?, last_name = ?
        WHERE id = ?
    """, (first_name, last_name, user_id))
    conn.commit()
    conn.close()
    
def update_admin_password(user_id, hashed_password):
    conn = get_db_connection()
    conn.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (hashed_password, user_id))
    conn.commit()
    conn.close()

def get_all_guides():
    conn = get_db_connection()
    guides = conn.execute("""
        SELECT id, first_name, last_name, email, languages
        FROM users
        WHERE role = 'guide'
    """).fetchall()
    conn.close()
    return [dict(guide) for guide in guides]

def get_all_participants():
    conn = get_db_connection()
    # Fetching all users with role 'participant'
    participants = conn.execute("SELECT id, first_name, last_name, email FROM users WHERE role = 'participant'").fetchall()
    conn.close()
    return [dict(row) for row in participants]