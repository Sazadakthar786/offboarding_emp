import os
from flask import Flask, render_template
from app.modules.hr import hr_bp
from app.modules.it import it_bp
from app.modules.finance import finance_bp
from app.modules.legal import legal_bp
from app.modules.admin import admin_bp
from app.modules.manager import manager_bp
from app.utils.data import load_employees

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.secret_key = 'supersecretkey'  # For session, flash, etc.

    # Register blueprints
    app.register_blueprint(hr_bp, url_prefix='/hr')
    app.register_blueprint(it_bp, url_prefix='/it')
    app.register_blueprint(finance_bp, url_prefix='/finance')
    app.register_blueprint(legal_bp, url_prefix='/legal')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(manager_bp, url_prefix='/manager')

    @app.route('/')
    def dashboard():
        employees = load_employees()
        return render_template('dashboard.html', employees=employees)

    return app 