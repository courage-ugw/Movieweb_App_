from flask import Blueprint, render_template

# Home page blueprint
home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static',
                    static_url_path='index_page/static', url_prefix='/')


@home_bp.route('/', methods=["GET"])
def home():
    return render_template('index.html')