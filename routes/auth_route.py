from flask import Blueprint, render_template,redirect,request,url_for,flash
from flask_login import login_user, logout_user, login_required
from dao.user_dao import verify_user

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = verify_user(email,password)
        if user:
            login_user(user)
            flash(f'Welcome, {user.first_name}!', 'success')
            if user.is_guide:
                return redirect(url_for('guides_dashboard'))
            return redirect(url_for('participants_dashboard'))
        flash("Invalid email or password credentials.", "danger")
    return render_template('login.html')    