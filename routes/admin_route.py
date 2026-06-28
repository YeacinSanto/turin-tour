from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps

from dao.admin_dao import get_admin_dashboard_stats,get_all_tours_summary,get_all_reservations_details,delete_tour_byId,update_tour_by_admin,update_admin_profile,update_admin_password, get_report


from dao.tours_dao import get_tour_complete_details
from werkzeug.security import generate_password_hash


admin_bp = Blueprint('admin_route', __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Access forbidden", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = get_admin_dashboard_stats()
    all_tours = get_all_tours_summary()
    reservations = get_all_reservations_details()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        all_tours=all_tours,
        reservations=reservations
    )



@admin_bp.route('/tour/delete/<int:tour_id>', methods=['POST'])
@admin_required
def delete_tour(tour_id):
    deleted = delete_tour_byId(tour_id)

    if deleted == 0:
        flash("Tour not found.", "warning")
    else:
        flash("Tour deleted successfully.", "success")

    return redirect(url_for('admin_route.dashboard'))


@admin_bp.route('/tour/edit/<int:tour_id>', methods=['GET', 'POST'])
@admin_required
def edit_tour(tour_id):

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            meeting_point = request.form.get('meeting_point')
            duration = int(request.form.get('duration'))
            language = request.form.get('language')
            max_participants = int(request.form.get('max_participants'))
            description = request.form.get('description')

            if not title or not meeting_point:
                flash("Title and meeting point are required.", "danger")
                return redirect(url_for('admin_route.edit_tour', tour_id=tour_id))

            update_tour_by_admin(
                tour_id,
                title,
                meeting_point,
                duration,
                language,
                max_participants,
                description
            )

            flash("Tour updated successfully.", "success")
            return redirect(url_for('admin_route.dashboard'))

        except (TypeError, ValueError):
            flash("Invalid numeric input.", "danger")
            return redirect(url_for('admin_route.edit_tour', tour_id=tour_id))

    tour = get_tour_complete_details(tour_id)
    return render_template('admin/edit_tour.html', tour=tour)

@admin_bp.route('/view-report/<int:report_id>', methods=["GET"])
@admin_required
def view_report(report_id):
    report = get_report(report_id)
    return render_template("view_report.html", report=report)

@admin_bp.route('/profile', methods=['GET', 'POST'])
@admin_required
def profile():

    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if not first_name or not last_name:
            flash("Name fields cannot be empty.", "danger")
            return redirect(url_for('admin_route.profile'))

        # Update profile
        update_admin_profile(current_user.id, first_name, last_name)

        # Password update
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                flash("Password confirmation mismatch.", "danger")
                return redirect(url_for('admin_route.profile'))

            hashed = generate_password_hash(new_password)
            update_admin_password(current_user.id, hashed)

        flash("Profile updated successfully.", "success")
        return redirect(url_for('admin_route.dashboard'))

    return render_template('admin/profile.html')