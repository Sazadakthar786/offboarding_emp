import json
import os
from typing import Dict, List, Any
from datetime import datetime
import uuid

class JSONHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the JSON file exists, create if it doesn't."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f, indent=4)

    def load_data(self) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_data(self, data: List[Dict[str, Any]]):
        """Save data to JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_employee_by_id(self, employee_id: str) -> Dict[str, Any]:
        """Get employee data by ID."""
        data = self.load_data()
        for employee in data:
            if employee["employee_id"] == employee_id:
                return employee
        return {}

    def get_employee_by_name(self, name: str) -> Dict[str, Any]:
        """Get employee data by name."""
        data = self.load_data()
        for employee in data:
            if employee["name"].lower() == name.lower():
                return employee
        return {}

    def update_employee(self, employee_id: str, updated_data: Dict[str, Any]):
        """Update employee data."""
        data = self.load_data()
        for i, employee in enumerate(data):
            if employee["employee_id"] == employee_id:
                data[i].update(updated_data)
                break
        self.save_data(data)

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Get all employees data."""
        return self.load_data()

    def get_employees_by_department(self, department: str) -> List[Dict[str, Any]]:
        """Get all employees in a specific department."""
        data = self.load_data()
        return [emp for emp in data if emp["department"] == department]

    def add_employee(self, employee_data: Dict[str, Any]) -> str:
        """Add a new employee to the database."""
        data = self.load_data()
        employee_id = str(uuid.uuid4())
        employee = {
            "employee_id": employee_id,
            "name": employee_data["name"],
            "email": employee_data["email"],
            "department": employee_data["department"],
            "position": employee_data["position"],
            "status": "Active",
            "join_date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        data.append(employee)
        self.save_data(data)
        return employee_id

    def create_offboarding_request(self, employee_id: str, request_data: Dict[str, Any]) -> str:
        """Create a new offboarding request."""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        request_id = str(uuid.uuid4())
        request = {
            "request_id": request_id,
            "employee_id": employee_id,
            "employee_name": employee["name"],
            "department": employee["department"],
            "last_working_day": request_data["last_working_day"],
            "reason": request_data["reason"],
            "notice_period": request_data["notice_period"],
            "status": "Pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "departments": {
                "hr": {"status": "Pending", "tasks": []},
                "it": {"status": "Pending", "tasks": []},
                "finance": {"status": "Pending", "tasks": []},
                "legal": {"status": "Pending", "tasks": []}
            }
        }

        # Update employee status
        self.update_employee(employee_id, {"status": "Resigned"})

        # Save request to offboarding requests file
        offboarding_file = os.path.join(os.path.dirname(self.file_path), 'offboarding_requests.json')
        handler = JSONHandler(offboarding_file)
        requests = handler.load_data()
        requests.append(request)
        handler.save_data(requests)

        return request_id

    def get_offboarding_requests(self) -> List[Dict[str, Any]]:
        """Get all offboarding requests."""
        offboarding_file = os.path.join(os.path.dirname(self.file_path), 'offboarding_requests.json')
        handler = JSONHandler(offboarding_file)
        return handler.load_data()

    def get_offboarding_request(self, request_id: str) -> Dict[str, Any]:
        """Get a specific offboarding request."""
        requests = self.get_offboarding_requests()
        for request in requests:
            if request["request_id"] == request_id:
                return request
        return {}

    def update_offboarding_request(self, request_id: str, updated_data: Dict[str, Any]):
        """Update an offboarding request."""
        offboarding_file = os.path.join(os.path.dirname(self.file_path), 'offboarding_requests.json')
        handler = JSONHandler(offboarding_file)
        requests = handler.load_data()
        
        for i, request in enumerate(requests):
            if request["request_id"] == request_id:
                requests[i].update(updated_data)
                requests[i]["updated_at"] = datetime.now().isoformat()
                break
        
        handler.save_data(requests)

    def create_exit_interview(self, employee_id: str, interview_data: Dict[str, Any]) -> str:
        """Create a new exit interview record."""
        interview_id = str(uuid.uuid4())
        interview = {
            "interview_id": interview_id,
            "employee_id": employee_id,
            "interview_date": interview_data["interview_date"],
            "interviewer": interview_data["interviewer"],
            "status": "Scheduled",
            "feedback": interview_data.get("feedback", ""),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # Save interview to exit interviews file
        interviews_file = os.path.join(os.path.dirname(self.file_path), 'exit_interviews.json')
        handler = JSONHandler(interviews_file)
        interviews = handler.load_data()
        interviews.append(interview)
        handler.save_data(interviews)

        return interview_id

    def get_exit_interviews(self) -> List[Dict[str, Any]]:
        """Get all exit interviews."""
        interviews_file = os.path.join(os.path.dirname(self.file_path), 'exit_interviews.json')
        handler = JSONHandler(interviews_file)
        return handler.load_data()

    def update_exit_interview(self, interview_id: str, updated_data: Dict[str, Any]):
        """Update an exit interview record."""
        interviews_file = os.path.join(os.path.dirname(self.file_path), 'exit_interviews.json')
        handler = JSONHandler(interviews_file)
        interviews = handler.load_data()
        
        for i, interview in enumerate(interviews):
            if interview["interview_id"] == interview_id:
                interviews[i].update(updated_data)
                interviews[i]["updated_at"] = datetime.now().isoformat()
                break
        
        handler.save_data(interviews) 