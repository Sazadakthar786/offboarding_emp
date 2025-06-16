from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from utils.json_handler import JSONHandler
from utils.offboarding_tracker import OffboardingTracker
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Path to employee data
DATA_PATH = os.path.join('data', 'employees.json')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

json_handler = JSONHandler(DATA_PATH)
offboarding_tracker = OffboardingTracker()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    employees = json_handler.get_all_employees()
    offboarding_requests = json_handler.get_offboarding_requests()
    return render_template('dashboard.html', 
                         active_item='dashboard', 
                         employees=employees,
                         offboarding_requests=offboarding_requests)

@app.route('/employees')
def all_employees():
    employees = json_handler.get_all_employees()
    return render_template('employees/all_employees.html', 
                         active_item='all_employees', 
                         employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        try:
            employee_data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'department': request.form['department'],
                'position': request.form['position']
            }
            employee_id = json_handler.add_employee(employee_data)
            flash('Employee added successfully!', 'success')
            return redirect(url_for('all_employees'))
        except Exception as e:
            flash(f'Error adding employee: {str(e)}', 'error')
    
    return render_template('employees/add_employee.html', active_item='add_employee')

@app.route('/offboarding/new', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        try:
            request_data = {
                'employee_id': request.form['employee'],
                'last_working_day': request.form['last_working_day'],
                'reason': request.form['reason'],
                'notice_period': int(request.form['notice_period'])
            }
            request_id = json_handler.create_offboarding_request(
                request_data['employee_id'], 
                request_data
            )
            flash('Offboarding request created successfully!', 'success')
            return redirect(url_for('status_tracker'))
        except Exception as e:
            flash(f'Error creating request: {str(e)}', 'error')
    
    employees = json_handler.get_all_employees()
    return render_template('offboarding/new_request.html', 
                         active_item='new_request',
                         employees=employees)

@app.route('/offboarding/status')
def status_tracker():
    offboarding_requests = json_handler.get_offboarding_requests()
    return render_template('offboarding/status_tracker.html', 
                         active_item='status_tracker',
                         offboarding_requests=offboarding_requests)

@app.route('/offboarding/interviews', methods=['GET', 'POST'])
def exit_interviews():
    if request.method == 'POST':
        try:
            interview_data = {
                'employee_id': request.form['employee_id'],
                'interview_date': request.form['interview_date'],
                'interviewer': request.form['interviewer'],
                'feedback': request.form.get('feedback', '')
            }
            interview_id = json_handler.create_exit_interview(
                interview_data['employee_id'],
                interview_data
            )
            flash('Exit interview scheduled successfully!', 'success')
            return redirect(url_for('exit_interviews'))
        except Exception as e:
            flash(f'Error scheduling interview: {str(e)}', 'error')
    
    exit_interviews = json_handler.get_exit_interviews()
    return render_template('offboarding/exit_interviews.html', 
                         active_item='exit_interviews',
                         exit_interviews=exit_interviews)

@app.route('/reports')
def reports():
    employees = json_handler.get_all_employees()
    offboarding_requests = json_handler.get_offboarding_requests()
    exit_interviews = json_handler.get_exit_interviews()
    
    # Calculate statistics
    total_employees = len(employees)
    active_employees = len([e for e in employees if e['status'] == 'Active'])
    pending_offboarding = len([r for r in offboarding_requests if r['status'] == 'Pending'])
    completed_offboarding = len([r for r in offboarding_requests if r['status'] == 'Completed'])
    
    return render_template('reports.html', 
                         active_item='reports',
                         total_employees=total_employees,
                         active_employees=active_employees,
                         pending_offboarding=pending_offboarding,
                         completed_offboarding=completed_offboarding)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', active_item='settings')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', active_item='contact')

@app.route('/employee/<employee_id>')
def employee_detail(employee_id):
    employee = json_handler.get_employee_by_id(employee_id)
    if not employee:
        flash('Employee not found', 'error')
        return redirect(url_for('all_employees'))
    
    # Get offboarding request if exists
    offboarding_requests = json_handler.get_offboarding_requests()
    offboarding_request = next(
        (r for r in offboarding_requests if r['employee_id'] == employee_id),
        None
    )
    
    return render_template('employee_detail.html', 
                         employee=employee,
                         offboarding_request=offboarding_request)

@app.route('/employee/<employee_id>/update_status', methods=['POST'])
def update_status(employee_id):
    new_status = request.form.get('status')
    if new_status in ['Active', 'Resigned']:
        employee = json_handler.get_employee_by_id(employee_id)
        if employee:
            employee['status'] = new_status
            json_handler.update_employee(employee_id, employee)
            flash(f'Status updated to {new_status}', 'success')
    return redirect(url_for('employee_detail', employee_id=employee_id))

@app.route('/employee/<employee_id>/upload_document', methods=['POST'])
def upload_document(employee_id):
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('employee_detail', employee_id=employee_id))
    
    file = request.files['file']
    doc_type = request.form.get('document_type')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{employee_id}_{doc_type}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Update employee record
        employee = json_handler.get_employee_by_id(employee_id)
        if employee:
            if doc_type == 'resignation':
                employee['resignation_letter'] = filename
            elif doc_type == 'exit_interview':
                employee['exit_interview'] = filename
            json_handler.update_employee(employee_id, employee)
            flash('Document uploaded successfully', 'success')
    else:
        flash('Invalid file type', 'error')
    
    return redirect(url_for('employee_detail', employee_id=employee_id))

@app.route('/offboarding/<request_id>/update_task', methods=['POST'])
def update_task(request_id):
    department = request.form.get('department')
    task = request.form.get('task')
    status = request.form.get('status')
    
    request_data = json_handler.get_offboarding_request(request_id)
    if request_data:
        if department in request_data['departments']:
            request_data['departments'][department]['status'] = status
            if task:
                request_data['departments'][department]['tasks'].append({
                    'task': task,
                    'status': status,
                    'updated_at': datetime.now().isoformat()
                })
            json_handler.update_offboarding_request(request_id, request_data)
            flash('Task status updated', 'success')
    
    return redirect(url_for('status_tracker'))

if __name__ == '__main__':
    app.run(debug=True) 