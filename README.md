<<<<<<< HEAD
# Employee Offboarding Portal

A Python GUI application for managing employee offboarding processes across different departments.

## Features

- Department-specific tabs for HR, IT, Finance, Legal, Admin, and Manager
- Employee selection and management
- Document upload/download functionality
- Status tracking and updates
- Employee table view
- Modular design for easy extension

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- Pillow (for image handling)
- ReportLab (for PDF generation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd offboarding-portal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. The application will open with tabs for each department and an employee table at the bottom.

3. Select an employee from the dropdown in any department tab to view their details and perform department-specific actions.

## Project Structure

```
offboarding_portal/
├── data/
│   └── sample_employees.json
├── modules/
│   ├── base_module.py
│   ├── hr_module.py
│   └── ... (other department modules)
├── utils/
│   └── json_handler.py
├── main.py
├── requirements.txt
└── README.md
```

## Department Modules

Each department module extends the base module and implements specific functionality:

- HR: Resignation letter submission, status updates, exit interview scheduling
- IT: System access revocation, device return, file backup
- Finance: Settlement calculation, loan management, final payslip generation
- Legal: NDA status, document return, dispute resolution
- Admin: Access card/key return, facility clearance
- Manager: Handover confirmation, exit checklist approval

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
=======
# Employee Offboarding Portal

A Python GUI application for managing employee offboarding processes across different departments.

## Features

- Department-specific tabs for HR, IT, Finance, Legal, Admin, and Manager
- Employee selection and management
- Document upload/download functionality
- Status tracking and updates
- Employee table view
- Modular design for easy extension

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- Pillow (for image handling)
- ReportLab (for PDF generation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd offboarding-portal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. The application will open with tabs for each department and an employee table at the bottom.

3. Select an employee from the dropdown in any department tab to view their details and perform department-specific actions.

## Project Structure

```
offboarding_portal/
├── data/
│   └── sample_employees.json
├── modules/
│   ├── base_module.py
│   ├── hr_module.py
│   └── ... (other department modules)
├── utils/
│   └── json_handler.py
├── main.py
├── requirements.txt
└── README.md
```

## Department Modules

Each department module extends the base module and implements specific functionality:

- HR: Resignation letter submission, status updates, exit interview scheduling
- IT: System access revocation, device return, file backup
- Finance: Settlement calculation, loan management, final payslip generation
- Legal: NDA status, document return, dispute resolution
- Admin: Access card/key return, facility clearance
- Manager: Handover confirmation, exit checklist approval

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
>>>>>>> 43451fc5cf1ae2c38def63e77b6905481892c38f
