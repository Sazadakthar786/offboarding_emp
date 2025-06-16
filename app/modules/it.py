from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.utils.data import load_employees, save_employees
import os

it_bp = Blueprint('it', __name__, template_folder='../../templates/it')

@it_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def it_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        emp['it_access_revoked'] = 'it_access_revoked' in request.form
        emp['devices_collected'] = 'devices_collected' in request.form
        emp['files_transferred'] = 'files_transferred' in request.form
        save_employees(employees)
        flash('IT info updated', 'success')
    return render_template('it/it_dashboard.html', emp=emp) 