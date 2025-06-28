from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.utils.data import load_employees, save_employees
import os

hr_bp = Blueprint('hr', __name__, template_folder='../../templates/hr')

@hr_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def hr_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Handle status update
        status = request.form.get('status')
        if status:
            emp['status'] = status
        # Handle resignation letter upload
        file = request.files.get('resignation_letter')
        if file and file.filename:
            filename = f"resignation_{emp_id}.pdf"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            emp['resignation_letter'] = filename
            flash('Resignation letter uploaded', 'success')
        # Handle exit interview date
        exit_interview = request.form.get('exit_interview')
        if exit_interview:
            emp['exit_interview'] = exit_interview
            flash('Exit interview scheduled', 'success')
        save_employees(employees)
        flash('HR info updated', 'success')
    return render_template('hr/hr_dashboard.html', emp=emp) 