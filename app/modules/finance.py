from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.utils.data import load_employees, save_employees
import os

finance_bp = Blueprint('finance', __name__, template_folder='../../templates/finance')

@finance_bp.route('/<int:emp_id>', methods=['GET', 'POST'])
def finance_dashboard(emp_id):
    employees = load_employees()
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        flash('Employee not found', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        if 'final_salary' in request.form:
            emp['final_salary'] = request.form.get('final_salary')
        if 'loan_balance' in request.form:
            emp['loan_balance'] = request.form.get('loan_balance')
        file = request.files.get('payslip')
        if file and file.filename:
            filename = f"payslip_{emp_id}.pdf"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            emp['payslip'] = filename
            flash('Payslip uploaded', 'success')
        save_employees(employees)
        flash('Finance info updated', 'success')
    return render_template('finance/finance_dashboard.html', emp=emp) 