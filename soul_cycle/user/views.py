from flask import Blueprint, render_template
from flask_login import login_required

from extensions import login_manager
from soul_cycle.api import login
from soul_cycle.user.models import User
from soul_cycle.user.forms import LoginForm

bp = Blueprint('user', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@bp.route('/')
@login_required
def home():
    return 'hello world!'

@bp.route('/user/login')
def login():
    form = LoginForm()
    return render_template('user/login.html', form=form)
