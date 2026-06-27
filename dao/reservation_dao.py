from dao.db import get_db_connection
from datetime import datetime, timedelta



def get_guide_tour_metrics(tour_id):
    conn = get_db_connection()
    # Fetch distinct operational dates booked so far
    dates_rows = conn.execute("SELECT DISTINCT tour_date FROM reservations WHERE tour_id = ? ORDER BY tour_date DESC", (tour_id,)).fetchall()
    
    metrics = []
    for d_row in dates_rows:
        date_str = d_row['tour_date']
        
        res_list = conn.execute("SELECT id, participant_id FROM reservations WHERE tour_id = ? AND tour_date = ?", (tour_id, date_str)).fetchall()
        
        total_p = 0
        bookings_manifest = []
        for r in res_list:
            p_user = conn.execute("SELECT first_name, last_name, email FROM users WHERE id = ?", (r['participant_id'],)).fetchone()
            guests = conn.execute("SELECT first_name, last_name FROM additional_participants WHERE reservation_id = ?", (r['id'],)).fetchall()
            
            guest_names = [f"{g['first_name']} {g['last_name']}" for g in guests]
            total_p += 1 + len(guests)
            
            bookings_manifest.append({
                'lead_name': f"{p_user['first_name']} {p_user['last_name']}",
                'lead_email': p_user['email'],
                'guests': guest_names,
                'count': 1 + len(guests)
            })
            
        # Is report filed already?
        rep = conn.execute("SELECT * FROM tour_reports WHERE tour_id = ? AND tour_date = ?", (tour_id, date_str)).fetchone()
        
        # Determine execution chronological completion
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        # For validation simplicity, historical dates are treated as report eligible
        is_past = parsed_date.date() <= datetime.now().date()

        metrics.append({
            'date': date_str,
            'total_expected': total_p,
            'manifest': bookings_manifest,
            'is_reported': rep is not None,
            'report_data': dict(rep) if rep else None,
            'eligible_for_report': is_past and (rep is None) and (total_p > 0)
        })
        
    conn.close()
    return metrics


def submit_tour_attendance_report(tour_id, date_string, head_count, image_filename):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO tour_reports (tour_id, tour_date, actual_count, report_image) VALUES (?, ?, ?, ?)",
            (tour_id, date_string, int(head_count), image_filename)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()