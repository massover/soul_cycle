from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask import current_app as app
from flask_login import login_required, login_user, logout_user
import requests

from extensions import login_manager, db
import soul_cycle.api
from soul_cycle.user.models import User
from soul_cycle.user.forms import LoginForm

bp = Blueprint('user', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@bp.route('/')
@login_required
def home():
    return render_template('home.html')

@bp.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            with soul_cycle.api.login(form.email.data, form.password.data) as s:
                if s.is_authenticated:
                    user = User.query.filter_by(email=form.email.data).first()
                    if user is None:
                        user = User(email=form.email.data)
                        db.session.add(user)
                        db.session.commit()
                    login_user(user)
                    return redirect(request.args.get('next') or url_for('.home'))
                else:
                    flash('Invalid email or password', 'danger')
        except requests.exceptions.RequestException as e:
            flash('Request error. Please try again later', 'danger')
        except (soul_cycle.api.ParsingError, soul_cycle.api.JsonResponseError) as e:
            flash('Request error. Please try again later', 'danger')
                    
    return render_template('user/login.html', form=form)

@bp.route('/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))    
