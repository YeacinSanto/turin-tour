
from flask import Blueprint,render_template
from flask_login import login_required, current_user
from dao.tours_dao import get_tours_by_guide, has_tour_reservations, create_tour, get_tour_complete_details,update_tour_full,update_tour_limited
from dao.reservation_dao import get_guide_tour_metrics

guides_bp = Blueprint('guides',__name__)

@guides_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_guid:
        return "Access Forbidden", 403
    tours = get_tours_by_guide(current_user)
    
    for tour in tours:
        tour['metrics'] = get_guide_tour_metrics(tour('id'))
    return render_template('guides_dashboard.html',tours=tours)