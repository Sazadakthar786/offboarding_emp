from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.data import load_employees, save_employees

manager_bp = Blueprint('manager', __name__, template_folder='../../templates/manager')

@manager_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def manager_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        emp['handover_confirmed'] = 'handover_confirmed' in request.form
        emp['checklist_approved'] = 'checklist_approved' in request.form
        save_employees(employees)
        flash('Manager info updated', 'success')
    return render_template('manager/manager_dashboard.html', emp=emp) 