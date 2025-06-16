from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.data import load_employees, save_employees

admin_bp = Blueprint('admin', __name__, template_folder='../../templates/admin')

@admin_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def admin_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        emp['access_card_reclaimed'] = 'access_card_reclaimed' in request.form
        emp['facility_access_removed'] = 'facility_access_removed' in request.form
        save_employees(employees)
        flash('Admin info updated', 'success')
    return render_template('admin/admin_dashboard.html', emp=emp) 