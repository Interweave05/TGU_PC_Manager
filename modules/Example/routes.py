from flask import Blueprint, render_template

example_bp = Blueprint('example', __name__, url_prefix='/example')

@example_bp.route('/')
def example_home():
    return render_template('example.html')
