from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.data import load_employees, save_employees

legal_bp = Blueprint('legal', __name__, template_folder='../../templates/legal')

@legal_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def legal_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        emp['nda_validated'] = 'nda_validated' in request.form
        emp['conf_docs_returned'] = 'conf_docs_returned' in request.form
        save_employees(employees)
        flash('Legal info updated', 'success')
    return render_template('legal/legal_dashboard.html', emp=emp) 