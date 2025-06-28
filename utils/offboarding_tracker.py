from typing import Dict, List, Any
from datetime import datetime

class OffboardingTracker:
    def __init__(self):
        self.departments = {
            "HR": {
                "tasks": [
                    "Submit Resignation Letter",
                    "Change Status to Resigned",
                    "Schedule Exit Interview"
                ]
            },
            "IT": {
                "tasks": [
                    "Revoke System Access",
                    "Return Company Device",
                    "Backup Files"
                ]
            },
            "Finance": {
                "tasks": [
                    "Calculate Settlement",
                    "Check Loans",
                    "Generate Final Payslip"
                ]
            },
            "Legal": {
                "tasks": [
                    "NDA Status Check",
                    "Document Return",
                    "Dispute Resolution"
                ]
            },
            "Admin": {
                "tasks": [
                    "Reclaim Access Cards/Keys",
                    "Facility Clearance"
                ]
            },
            "Manager": {
                "tasks": [
                    "Confirm Handover",
                    "Approve Exit Checklist"
                ]
            }
        }

    def initialize_employee_tracking(self, employee_id: str) -> Dict[str, Any]:
        """Initialize tracking for a new employee offboarding process."""
        tracking_data = {
            "employee_id": employee_id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "In Progress",
            "departments": {}
        }

        for dept, info in self.departments.items():
            tracking_data["departments"][dept] = {
                "status": "Pending",
                "tasks": {task: "Pending" for task in info["tasks"]},
                "completed_date": None
            }

        return tracking_data

    def update_task_status(self, tracking_data: Dict[str, Any], department: str, task: str, status: str = "Completed"):
        """Update the status of a specific task for a department."""
        if department in tracking_data["departments"] and task in tracking_data["departments"][department]["tasks"]:
            tracking_data["departments"][department]["tasks"][task] = status
            
            # Check if all tasks in department are completed
            all_completed = all(task_status == "Completed" 
                              for task_status in tracking_data["departments"][department]["tasks"].values())
            
            if all_completed:
                tracking_data["departments"][department]["status"] = "Completed"
                tracking_data["departments"][department]["completed_date"] = datetime.now().strftime("%Y-%m-%d")
            
            # Check if all departments are completed
            all_depts_completed = all(dept["status"] == "Completed" 
                                    for dept in tracking_data["departments"].values())
            
            if all_depts_completed:
                tracking_data["status"] = "Completed"

        return tracking_data

    def get_department_progress(self, tracking_data: Dict[str, Any], department: str) -> Dict[str, Any]:
        """Get the progress of a specific department."""
        if department in tracking_data["departments"]:
            dept_data = tracking_data["departments"][department]
            total_tasks = len(dept_data["tasks"])
            completed_tasks = sum(1 for status in dept_data["tasks"].values() if status == "Completed")
            
            return {
                "status": dept_data["status"],
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks,
                "tasks": dept_data["tasks"],
                "completed_date": dept_data["completed_date"]
            }
        return {}

    def get_overall_progress(self, tracking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get the overall progress of the offboarding process."""
        total_tasks = sum(len(dept["tasks"]) for dept in self.departments.values())
        completed_tasks = sum(
            sum(1 for task_status in dept_data["tasks"].values() if task_status == "Completed")
            for dept_data in tracking_data["departments"].values()
        )

        return {
            "status": tracking_data["status"],
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "start_date": tracking_data["start_date"],
            "departments": {
                dept: self.get_department_progress(tracking_data, dept)
                for dept in self.departments.keys()
            }
        } 