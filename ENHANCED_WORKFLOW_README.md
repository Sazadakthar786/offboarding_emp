# Enhanced Employee Offboarding Workflow System

## Overview

This enhanced offboarding workflow system implements a comprehensive, structured approach to employee offboarding with clear team responsibilities, automatic due date calculation, and comprehensive tracking. The system is designed to streamline the offboarding process and ensure all necessary steps are completed in a timely manner.

## 🏗️ Architecture

### Core Components

1. **EnhancedOffboardingWorkflow Class** (`modules/enhanced_workflow.py`)
   - Main workflow engine
   - Handles workflow creation, task management, and status tracking
   - Manages team responsibilities and due dates

2. **Flask Web Application** (`app.py`)
   - Web interface for the workflow system
   - RESTful API endpoints for workflow management
   - Integration with existing offboarding portal

3. **HTML Templates** (`templates/enhanced_offboarding/`)
   - User interface for workflow management
   - Status tracking and task updates
   - Team-specific views

## 📋 Workflow Structure

The enhanced workflow consists of **7 structured steps** with clear team responsibilities and timing:

### Step 1: Initial Request (Line Manager) - Day 0
**Responsible Team:** Line Manager
- **Tasks:**
  - Capture Employee Details (ID, Name, Email, LWD, Reason for Leaving)
  - Validate Request

### Step 2: People Ops Review - Within 1 Day
**Responsible Team:** People Ops
- **Tasks:**
  - Review Employee Details
  - Secure Signed Documents
  - Raise IT Ticket (Azure)

### Step 3: Pre-LWD Processing - 1 Week Before LWD
**Responsible Teams:** People Ops, Corporate Development, Finance
- **People Ops Tasks:**
  - Process Termination in ZenHR
  - Cancel Insurance, GOSI, Qiwa
  - Calculate EOS (End of Service)
  - Notify Corporate Development
- **Corporate Development Tasks:**
  - Handle Equity Matters
  - Update Personal Email
- **Finance Tasks:**
  - Close HALA Card
  - Settle Loans

### Step 4: LWD Processing (IT & Facilities) - On LWD
**Responsible Teams:** IT, Facilities
- **IT Tasks:**
  - Revoke System Access
  - Backup Employee Files
  - Collect Company Devices
- **Facilities Tasks:**
  - Collect Access Cards
  - Collect Parking Permits
  - Collect Other Property

### Step 5: Exit Interview (HR) - On LWD
**Responsible Team:** HR
- **Tasks:**
  - Conduct Exit Interview
  - Collect Feedback
  - Document Interview

### Step 6: Post-LWD Processing - 1 Week After LWD
**Responsible Teams:** Finance, People Ops
- **Finance Tasks:**
  - Process Final Payment
- **People Ops Tasks:**
  - Provide Experience Certificate
  - Provide Reference Documents

### Step 7: Final Closure (People Ops) - After All Steps
**Responsible Team:** People Ops
- **Tasks:**
  - Verify All Steps Completed
  - Close Jira Ticket
  - Archive Employee Files

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Required packages (see `requirements.txt`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd offboarding_portal
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the web interface:**
   - Open your browser and go to `http://localhost:5000`
   - Navigate to "Enhanced Offboarding" section

### Running the Test Script

To test the enhanced workflow system:

```bash
python test_enhanced_workflow.py
```

This will create sample workflows, update tasks, and demonstrate all features.

## 📖 Usage Guide

### Creating a New Enhanced Workflow

1. **Navigate to Enhanced Offboarding:**
   - Go to Dashboard → "New Enhanced Request"
   - Or directly visit `/enhanced-offboarding/new`

2. **Fill in Employee Details:**
   - Employee ID, Name, Email (required)
   - Last Working Day (required)
   - Reason for Leaving (dropdown selection)
   - Additional information (optional)

3. **Submit the Request:**
   - The system automatically calculates due dates
   - Creates all workflow steps and tasks
   - Assigns team responsibilities

### Managing Workflows

#### View All Workflows
- Visit `/enhanced-offboarding/status`
- See all active workflows with progress indicators
- Filter by status, team, or date

#### View Workflow Details
- Click on any workflow to see detailed view
- View all steps and tasks
- Update task status
- Add notes and comments

#### Team-Specific Views
- **People Ops:** `/enhanced-offboarding/team/people_ops`
- **IT:** `/enhanced-offboarding/team/it`
- **Finance:** `/enhanced-offboarding/team/finance`
- **HR:** `/enhanced-offboarding/team/hr`

#### Overdue Tasks
- Visit `/enhanced-offboarding/overdue`
- See all tasks that have passed their due date
- Take immediate action on urgent items

### Updating Task Status

1. **Navigate to Workflow Detail:**
   - Click on any workflow from the status tracker

2. **Update Task Status:**
   - Click "Update" button on any task
   - Select new status (Pending, In Progress, Completed, etc.)
   - Add completion notes
   - Specify who completed the task

3. **Automatic Progress Tracking:**
   - System automatically updates overall progress
   - Step completion is tracked
   - Workflow completion is determined

## 🔧 API Endpoints

### Workflow Management

- `POST /enhanced-offboarding/new` - Create new workflow
- `GET /enhanced-offboarding/status` - List all workflows
- `GET /enhanced-offboarding/<request_id>` - Get workflow details
- `POST /enhanced-offboarding/<request_id>/update-task` - Update task status
- `POST /enhanced-offboarding/<request_id>/add-note` - Add workflow note

### Team Views

- `GET /enhanced-offboarding/team/<team_name>` - Get team tasks
- `GET /enhanced-offboarding/overdue` - Get overdue tasks

### Reporting

- `GET /enhanced-offboarding/<request_id>/export` - Export workflow report (JSON)

## 📊 Features

### ✅ Core Features

- **Structured Workflow:** 7 clearly defined steps with team responsibilities
- **Automatic Due Dates:** Calculated based on Last Working Day
- **Team Task Assignment:** Clear responsibility assignment
- **Progress Tracking:** Real-time progress updates
- **Status Management:** Multiple status levels (Pending, In Progress, Completed, etc.)
- **Notes System:** Add comments and notes to workflows and tasks
- **Overdue Detection:** Automatic identification of overdue tasks
- **Export Functionality:** Generate comprehensive reports

### ✅ Advanced Features

- **Task Dependencies:** Some tasks depend on others being completed
- **Team Filtering:** View tasks by specific teams
- **Comprehensive Reporting:** Detailed workflow reports
- **Web Interface:** User-friendly web application
- **RESTful API:** Programmatic access to workflow data
- **Error Handling:** Robust error handling and validation
- **Logging:** Comprehensive logging for debugging

### ✅ User Experience

- **Responsive Design:** Works on desktop and mobile
- **Intuitive Interface:** Easy-to-use web interface
- **Visual Progress Indicators:** Clear progress bars and status badges
- **Quick Actions:** Fast access to common tasks
- **Search and Filter:** Easy workflow discovery

## 🏛️ Team Responsibilities

### Line Manager
- Initiates offboarding process
- Provides employee information
- Validates request details

### People Ops
- Reviews and processes employee details
- Manages documentation
- Coordinates with other teams
- Handles final closure

### IT
- Manages system access
- Handles device collection
- Backs up employee data

### Facilities
- Collects physical assets
- Manages access cards and permits
- Handles facility clearance

### Corporate Development
- Manages equity matters
- Updates personal email addresses
- Handles equity-related communications

### Finance
- Processes final payments
- Manages loan settlements
- Closes financial accounts

### HR
- Conducts exit interviews
- Collects feedback
- Documents interview process

## 📈 Benefits

### For Organizations
- **Standardized Process:** Consistent offboarding across all departments
- **Compliance:** Ensures all legal and regulatory requirements are met
- **Efficiency:** Reduces manual coordination and follow-up
- **Transparency:** Clear visibility into process status
- **Risk Mitigation:** Prevents missed steps and compliance issues

### For Teams
- **Clear Responsibilities:** Each team knows exactly what they need to do
- **Timeline Management:** Automatic due dates prevent delays
- **Progress Tracking:** Real-time visibility into task completion
- **Communication:** Built-in notes and comments system

### For Employees
- **Smooth Transition:** Well-organized offboarding process
- **Clear Timeline:** Know what to expect and when
- **Professional Experience:** Structured and professional approach

## 🔮 Future Enhancements

### Planned Features
- **Email Notifications:** Automatic email alerts for due dates and completions
- **Calendar Integration:** Sync with team calendars
- **Mobile App:** Native mobile application
- **Advanced Reporting:** Analytics and insights
- **Integration APIs:** Connect with HRIS and other systems
- **Workflow Templates:** Customizable workflow templates
- **Multi-language Support:** Internationalization

### Technical Improvements
- **Database Integration:** Persistent storage
- **Real-time Updates:** WebSocket integration
- **Advanced Security:** Role-based access control
- **API Documentation:** Swagger/OpenAPI documentation
- **Performance Optimization:** Caching and optimization

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- Check the documentation
- Review the test script for examples
- Open an issue on GitHub
- Contact the development team

### Common Issues
- **Import Errors:** Ensure all dependencies are installed
- **Template Errors:** Check that all template files are in the correct location
- **Workflow Creation Errors:** Verify all required fields are provided

## 📞 Contact

For questions, suggestions, or support:
- Email: [your-email@company.com]
- GitHub Issues: [repository-issues-url]
- Documentation: [documentation-url]

---

**Built with ❤️ for better employee experiences** 