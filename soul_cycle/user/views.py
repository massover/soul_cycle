from flask import Blueprint
from extensions import login_manager
from .models import User

bp = Blueprint('user', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@bp.route('/')
def home():
    return 'hello world!'

@bp.route('/user/login')
def login():
    return 'hello world!'
