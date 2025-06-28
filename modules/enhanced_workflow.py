"""
Enhanced Employee Offboarding Workflow Module
============================================

This module implements a comprehensive, structured employee offboarding workflow
with clear team responsibilities and timing requirements.

Workflow Overview:
1. Initial Request (Line Manager) - Day 0
2. People Ops Review (Within 1 day)
3. Pre-LWD Processing (1 week before LWD)
4. LWD Processing (IT & Facilities)
5. Exit Interview (HR on LWD)
6. Post-LWD Processing (1 week after)
7. Final Closure (People Ops)

Each step is clearly defined with responsible teams and specific tasks.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    BLOCKED = "blocked"


class TeamResponsibility(Enum):
    """Team responsibility enumeration."""
    LINE_MANAGER = "line_manager"
    PEOPLE_OPS = "people_ops"
    IT = "it"
    FACILITIES = "facilities"
    CORPORATE_DEVELOPMENT = "corporate_development"
    FINANCE = "finance"
    HR = "hr"


class ReasonForLeaving(Enum):
    """Reason for leaving enumeration."""
    TERMINATION = "termination"
    RESIGNATION = "resignation"
    NON_RENEWAL = "non_renewal"
    MUTUAL_AGREEMENT = "mutual_agreement"


class EnhancedOffboardingWorkflow:
    """
    Enhanced Employee Offboarding Workflow System
    
    Implements a comprehensive, structured workflow with clear team responsibilities,
    timing requirements, and task dependencies.
    """
    
    def __init__(self):
        """Initialize the enhanced workflow system."""
        self.workflow_steps = self._initialize_workflow_steps()
        self.active_workflows = {}
        
    def _initialize_workflow_steps(self) -> Dict[str, Dict]:
        """
        Initialize the complete workflow structure with all steps, teams, and timing.
        
        Returns:
            Dict containing all workflow steps with their configurations
        """
        return {
            "step_1_initial_request": {
                "name": "Initial Request by Line Manager",
                "responsible_team": TeamResponsibility.LINE_MANAGER,
                "timing": "Day 0",
                "description": "Line Manager initiates offboarding request with employee details",
                "tasks": [
                    {
                        "id": "capture_employee_details",
                        "name": "Capture Employee Details",
                        "description": "Collect employee ID, name, email, LWD, and reason for leaving",
                        "required_fields": ["employee_id", "name", "email", "last_working_day", "reason_for_leaving"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "validate_request",
                        "name": "Validate Request",
                        "description": "Ensure all required information is complete and accurate",
                        "dependencies": ["capture_employee_details"],
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_2_people_ops_review": {
                "name": "People Ops Review and Documentation",
                "responsible_team": TeamResponsibility.PEOPLE_OPS,
                "timing": "Within 1 day",
                "description": "People Ops reviews details and secures required documents",
                "tasks": [
                    {
                        "id": "review_employee_details",
                        "name": "Review Employee Details",
                        "description": "Review and validate all submitted employee information",
                        "dependencies": ["step_1_initial_request"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "secure_signed_documents",
                        "name": "Secure Signed Documents",
                        "description": "Collect and verify all required signed documents",
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "raise_it_ticket",
                        "name": "Raise IT Ticket (Azure)",
                        "description": "Create IT ticket in Azure for access revocation and device collection",
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_3_pre_lwd_processing": {
                "name": "Pre-LWD Processing (1 week before LWD)",
                "responsible_team": [TeamResponsibility.PEOPLE_OPS, TeamResponsibility.CORPORATE_DEVELOPMENT, TeamResponsibility.FINANCE],
                "timing": "1 week before LWD",
                "description": "Process termination in systems and handle equity/financial matters",
                "tasks": [
                    {
                        "id": "process_zenhr_termination",
                        "name": "Process Termination in ZenHR",
                        "description": "Update employee status in ZenHR system",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "cancel_insurance_gosi_qiwa",
                        "name": "Cancel Insurance, GOSI, Qiwa",
                        "description": "Cancel employee benefits and government registrations",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "calculate_eos",
                        "name": "Calculate EOS (End of Service)",
                        "description": "Calculate end of service benefits",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "notify_corporate_dev",
                        "name": "Notify Corporate Development",
                        "description": "Inform Corporate Development team about employee departure",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "handle_equity_matters",
                        "name": "Handle Equity Matters",
                        "description": "Process equity-related matters and updates",
                        "responsible_team": TeamResponsibility.CORPORATE_DEVELOPMENT,
                        "dependencies": ["notify_corporate_dev"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "update_personal_email",
                        "name": "Update Personal Email",
                        "description": "Update employee's personal email for future communications",
                        "responsible_team": TeamResponsibility.CORPORATE_DEVELOPMENT,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "close_hala_card",
                        "name": "Close HALA Card",
                        "description": "Close employee's HALA card account",
                        "responsible_team": TeamResponsibility.FINANCE,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "settle_loans",
                        "name": "Settle Loans",
                        "description": "Process any outstanding loan settlements",
                        "responsible_team": TeamResponsibility.FINANCE,
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_4_lwd_it_facilities": {
                "name": "LWD Processing (IT & Facilities)",
                "responsible_team": [TeamResponsibility.IT, TeamResponsibility.FACILITIES],
                "timing": "On LWD",
                "description": "IT revokes access and collects devices, Facilities collects property",
                "tasks": [
                    {
                        "id": "revoke_system_access",
                        "name": "Revoke System Access",
                        "description": "Revoke all system and application access",
                        "responsible_team": TeamResponsibility.IT,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "backup_employee_files",
                        "name": "Backup Employee Files",
                        "description": "Create backup of employee's work files and data",
                        "responsible_team": TeamResponsibility.IT,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "collect_company_devices",
                        "name": "Collect Company Devices",
                        "description": "Collect all company-issued devices (laptop, phone, etc.)",
                        "responsible_team": TeamResponsibility.IT,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "collect_access_cards",
                        "name": "Collect Access Cards",
                        "description": "Collect building and system access cards",
                        "responsible_team": TeamResponsibility.FACILITIES,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "collect_parking_permits",
                        "name": "Collect Parking Permits",
                        "description": "Collect parking permits and related items",
                        "responsible_team": TeamResponsibility.FACILITIES,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "collect_other_property",
                        "name": "Collect Other Property",
                        "description": "Collect any other company property (keys, equipment, etc.)",
                        "responsible_team": TeamResponsibility.FACILITIES,
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_5_exit_interview": {
                "name": "Exit Interview (HR)",
                "responsible_team": TeamResponsibility.HR,
                "timing": "On LWD",
                "description": "Conduct exit interview and collect feedback",
                "tasks": [
                    {
                        "id": "conduct_exit_interview",
                        "name": "Conduct Exit Interview",
                        "description": "Conduct comprehensive exit interview with employee",
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "collect_feedback",
                        "name": "Collect Feedback",
                        "description": "Document employee feedback and suggestions",
                        "dependencies": ["conduct_exit_interview"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "document_interview",
                        "name": "Document Interview",
                        "description": "Create official documentation of exit interview",
                        "dependencies": ["collect_feedback"],
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_6_post_lwd_processing": {
                "name": "Post-LWD Processing (1 week after)",
                "responsible_team": [TeamResponsibility.FINANCE, TeamResponsibility.PEOPLE_OPS],
                "timing": "1 week after LWD",
                "description": "Process final payment and provide experience certificate",
                "tasks": [
                    {
                        "id": "process_final_payment",
                        "name": "Process Final Payment",
                        "description": "Process and release final salary and benefits payment",
                        "responsible_team": TeamResponsibility.FINANCE,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "provide_experience_certificate",
                        "name": "Provide Experience Certificate",
                        "description": "Generate and provide experience certificate",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "provide_reference_documents",
                        "name": "Provide Reference Documents",
                        "description": "Prepare and provide reference letters and documents",
                        "responsible_team": TeamResponsibility.PEOPLE_OPS,
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            },
            
            "step_7_final_closure": {
                "name": "Final Closure (People Ops)",
                "responsible_team": TeamResponsibility.PEOPLE_OPS,
                "timing": "After all steps completed",
                "description": "Confirm all steps completed and close the process",
                "tasks": [
                    {
                        "id": "verify_all_steps_completed",
                        "name": "Verify All Steps Completed",
                        "description": "Review and verify all workflow steps are completed",
                        "dependencies": ["step_1_initial_request", "step_2_people_ops_review", 
                                       "step_3_pre_lwd_processing", "step_4_lwd_it_facilities",
                                       "step_5_exit_interview", "step_6_post_lwd_processing"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "close_jira_ticket",
                        "name": "Close Jira Ticket",
                        "description": "Close the offboarding ticket in Jira system",
                        "dependencies": ["verify_all_steps_completed"],
                        "status": WorkflowStatus.PENDING
                    },
                    {
                        "id": "archive_employee_files",
                        "name": "Archive Employee Files",
                        "description": "Archive all employee-related files and documents",
                        "dependencies": ["verify_all_steps_completed"],
                        "status": WorkflowStatus.PENDING
                    }
                ],
                "status": WorkflowStatus.PENDING,
                "due_date": None
            }
        }
    
    def create_offboarding_request(self, employee_data: Dict[str, Any]) -> str:
        """
        Create a new offboarding request with the enhanced workflow.
        
        Args:
            employee_data: Dictionary containing employee information
                - employee_id: Employee ID
                - name: Employee name
                - email: Employee email
                - last_working_day: Last working day (YYYY-MM-DD)
                - reason_for_leaving: Reason for leaving (from ReasonForLeaving enum)
                - line_manager: Line manager name
                - department: Employee department
                - position: Employee position
        
        Returns:
            str: Request ID for the created offboarding request
        """
        try:
            # Validate required fields
            required_fields = ["employee_id", "name", "email", "last_working_day", "reason_for_leaving"]
            for field in required_fields:
                if field not in employee_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate reason for leaving
            if employee_data["reason_for_leaving"] not in [reason.value for reason in ReasonForLeaving]:
                raise ValueError(f"Invalid reason for leaving: {employee_data['reason_for_leaving']}")
            
            # Generate request ID
            request_id = f"OB-{employee_data['employee_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate due dates based on LWD
            lwd = datetime.strptime(employee_data["last_working_day"], "%Y-%m-%d")
            
            # Initialize workflow with calculated due dates
            workflow_data = {
                "request_id": request_id,
                "employee_data": employee_data,
                "created_date": datetime.now().isoformat(),
                "status": WorkflowStatus.PENDING.value,
                "steps": self._initialize_workflow_with_dates(lwd),
                "current_step": "step_1_initial_request",
                "overall_progress": 0,
                "notes": [],
                "attachments": []
            }
            
            # Store workflow
            self.active_workflows[request_id] = workflow_data
            
            logger.info(f"Created offboarding request {request_id} for employee {employee_data['employee_id']}")
            
            return request_id
            
        except Exception as e:
            logger.error(f"Error creating offboarding request: {str(e)}")
            raise
    
    def _initialize_workflow_with_dates(self, lwd: datetime) -> Dict[str, Any]:
        """
        Initialize workflow steps with calculated due dates based on LWD.
        
        Args:
            lwd: Last working day datetime object
            
        Returns:
            Dict containing workflow steps with calculated due dates
        """
        workflow_steps = {}
        
        for step_id, step_config in self.workflow_steps.items():
            step_data = step_config.copy()
            
            # Calculate due dates based on timing requirements
            if step_id == "step_1_initial_request":
                step_data["due_date"] = datetime.now().isoformat()
            elif step_id == "step_2_people_ops_review":
                step_data["due_date"] = (datetime.now() + timedelta(days=1)).isoformat()
            elif step_id == "step_3_pre_lwd_processing":
                step_data["due_date"] = (lwd - timedelta(days=7)).isoformat()
            elif step_id == "step_4_lwd_it_facilities":
                step_data["due_date"] = lwd.isoformat()
            elif step_id == "step_5_exit_interview":
                step_data["due_date"] = lwd.isoformat()
            elif step_id == "step_6_post_lwd_processing":
                step_data["due_date"] = (lwd + timedelta(days=7)).isoformat()
            elif step_id == "step_7_final_closure":
                step_data["due_date"] = (lwd + timedelta(days=14)).isoformat()
            
            # Initialize task statuses
            for task in step_data["tasks"]:
                task["status"] = WorkflowStatus.PENDING.value
                task["completed_date"] = None
                task["completed_by"] = None
                task["notes"] = []
            
            workflow_steps[step_id] = step_data
        
        return workflow_steps
    
    def update_task_status(self, request_id: str, step_id: str, task_id: str, 
                          status: WorkflowStatus, completed_by: str = None, notes: str = None) -> bool:
        """
        Update the status of a specific task in the workflow.
        
        Args:
            request_id: The offboarding request ID
            step_id: The step ID within the workflow
            task_id: The task ID within the step
            status: New status for the task
            completed_by: Name/ID of person completing the task
            notes: Additional notes about the task completion
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if request_id not in self.active_workflows:
                raise ValueError(f"Request ID {request_id} not found")
            
            workflow = self.active_workflows[request_id]
            
            if step_id not in workflow["steps"]:
                raise ValueError(f"Step ID {step_id} not found in workflow")
            
            step = workflow["steps"][step_id]
            
            # Find the task
            task = None
            for t in step["tasks"]:
                if t["id"] == task_id:
                    task = t
                    break
            
            if not task:
                raise ValueError(f"Task ID {task_id} not found in step {step_id}")
            
            # Update task status
            task["status"] = status.value
            if status == WorkflowStatus.COMPLETED:
                task["completed_date"] = datetime.now().isoformat()
                task["completed_by"] = completed_by
            
            if notes:
                task["notes"].append({
                    "date": datetime.now().isoformat(),
                    "note": notes,
                    "added_by": completed_by
                })
            
            # Check if all tasks in step are completed
            all_tasks_completed = all(t["status"] == WorkflowStatus.COMPLETED.value for t in step["tasks"])
            if all_tasks_completed:
                step["status"] = WorkflowStatus.COMPLETED.value
                step["completed_date"] = datetime.now().isoformat()
            
            # Update overall progress
            self._update_overall_progress(workflow)
            
            logger.info(f"Updated task {task_id} in step {step_id} for request {request_id} to {status.value}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating task status: {str(e)}")
            return False
    
    def _update_overall_progress(self, workflow: Dict[str, Any]) -> None:
        """
        Update the overall progress of the workflow.
        
        Args:
            workflow: The workflow data dictionary
        """
        total_tasks = 0
        completed_tasks = 0
        
        for step in workflow["steps"].values():
            for task in step["tasks"]:
                total_tasks += 1
                if task["status"] == WorkflowStatus.COMPLETED.value:
                    completed_tasks += 1
        
        if total_tasks > 0:
            workflow["overall_progress"] = (completed_tasks / total_tasks) * 100
        
        # Check if workflow is complete
        all_steps_completed = all(step["status"] == WorkflowStatus.COMPLETED.value 
                                for step in workflow["steps"].values())
        
        if all_steps_completed:
            workflow["status"] = WorkflowStatus.COMPLETED.value
    
    def get_workflow_status(self, request_id: str) -> Dict[str, Any]:
        """
        Get the current status of a workflow.
        
        Args:
            request_id: The offboarding request ID
            
        Returns:
            Dict containing workflow status and progress information
        """
        if request_id not in self.active_workflows:
            raise ValueError(f"Request ID {request_id} not found")
        
        workflow = self.active_workflows[request_id]
        
        return {
            "request_id": request_id,
            "employee_data": workflow["employee_data"],
            "status": workflow["status"],
            "overall_progress": workflow["overall_progress"],
            "created_date": workflow["created_date"],
            "current_step": workflow["current_step"],
            "steps": workflow["steps"],
            "notes": workflow["notes"]
        }
    
    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all overdue tasks across all workflows.
        
        Returns:
            List of overdue tasks with workflow and employee information
        """
        overdue_tasks = []
        current_date = datetime.now()
        
        for request_id, workflow in self.active_workflows.items():
            for step_id, step in workflow["steps"].items():
                if step["status"] != WorkflowStatus.COMPLETED.value:
                    due_date = datetime.fromisoformat(step["due_date"])
                    if due_date < current_date:
                        overdue_tasks.append({
                            "request_id": request_id,
                            "employee_name": workflow["employee_data"]["name"],
                            "employee_id": workflow["employee_data"]["employee_id"],
                            "step_id": step_id,
                            "step_name": step["name"],
                            "responsible_team": step["responsible_team"],
                            "due_date": step["due_date"],
                            "days_overdue": (current_date - due_date).days
                        })
        
        return overdue_tasks
    
    def get_tasks_by_team(self, team: TeamResponsibility) -> List[Dict[str, Any]]:
        """
        Get all tasks assigned to a specific team.
        
        Args:
            team: The team responsibility to filter by
            
        Returns:
            List of tasks assigned to the specified team
        """
        team_tasks = []
        
        for request_id, workflow in self.active_workflows.items():
            for step_id, step in workflow["steps"].items():
                # Check if team is responsible for this step
                step_teams = step["responsible_team"]
                if isinstance(step_teams, list):
                    if team in step_teams:
                        for task in step["tasks"]:
                            if task.get("responsible_team") == team or task.get("responsible_team") is None:
                                team_tasks.append({
                                    "request_id": request_id,
                                    "employee_name": workflow["employee_data"]["name"],
                                    "employee_id": workflow["employee_data"]["employee_id"],
                                    "step_id": step_id,
                                    "step_name": step["name"],
                                    "task_id": task["id"],
                                    "task_name": task["name"],
                                    "task_description": task["description"],
                                    "status": task["status"],
                                    "due_date": step["due_date"],
                                    "completed_date": task["completed_date"],
                                    "completed_by": task["completed_by"]
                                })
                elif step_teams == team:
                    for task in step["tasks"]:
                        team_tasks.append({
                            "request_id": request_id,
                            "employee_name": workflow["employee_data"]["name"],
                            "employee_id": workflow["employee_data"]["employee_id"],
                            "step_id": step_id,
                            "step_name": step["name"],
                            "task_id": task["id"],
                            "task_name": task["name"],
                            "task_description": task["description"],
                            "status": task["status"],
                            "due_date": step["due_date"],
                            "completed_date": task["completed_date"],
                            "completed_by": task["completed_by"]
                        })
        
        return team_tasks
    
    def add_note_to_workflow(self, request_id: str, note: str, added_by: str) -> bool:
        """
        Add a note to the workflow.
        
        Args:
            request_id: The offboarding request ID
            note: The note content
            added_by: Name/ID of person adding the note
            
        Returns:
            bool: True if note was added successfully, False otherwise
        """
        try:
            if request_id not in self.active_workflows:
                raise ValueError(f"Request ID {request_id} not found")
            
            workflow = self.active_workflows[request_id]
            
            workflow["notes"].append({
                "date": datetime.now().isoformat(),
                "note": note,
                "added_by": added_by
            })
            
            logger.info(f"Added note to workflow {request_id} by {added_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding note to workflow: {str(e)}")
            return False
    
    def export_workflow_report(self, request_id: str) -> Dict[str, Any]:
        """
        Export a comprehensive report for a workflow.
        
        Args:
            request_id: The offboarding request ID
            
        Returns:
            Dict containing comprehensive workflow report
        """
        if request_id not in self.active_workflows:
            raise ValueError(f"Request ID {request_id} not found")
        
        workflow = self.active_workflows[request_id]
        
        report = {
            "request_id": request_id,
            "employee_data": workflow["employee_data"],
            "workflow_summary": {
                "status": workflow["status"],
                "overall_progress": workflow["overall_progress"],
                "created_date": workflow["created_date"],
                "current_step": workflow["current_step"]
            },
            "steps_detail": {},
            "team_summary": {},
            "timeline": []
        }
        
        # Process each step
        for step_id, step in workflow["steps"].items():
            # Convert TeamResponsibility to string for JSON serialization
            responsible_team = step["responsible_team"]
            if isinstance(responsible_team, list):
                responsible_team_str = [team.value if hasattr(team, 'value') else str(team) for team in responsible_team]
            else:
                responsible_team_str = responsible_team.value if hasattr(responsible_team, 'value') else str(responsible_team)
            
            step_detail = {
                "name": step["name"],
                "responsible_team": responsible_team_str,
                "status": step["status"],
                "due_date": step["due_date"],
                "completed_date": step.get("completed_date"),
                "tasks": step["tasks"]
            }
            
            report["steps_detail"][step_id] = step_detail
            
            # Add to timeline
            if step["status"] == WorkflowStatus.COMPLETED.value:
                report["timeline"].append({
                    "date": step["completed_date"],
                    "action": f"Completed: {step['name']}",
                    "team": responsible_team_str
                })
        
        # Generate team summary
        team_tasks = {}
        for step in workflow["steps"].values():
            teams = step["responsible_team"] if isinstance(step["responsible_team"], list) else [step["responsible_team"]]
            for team in teams:
                team_key = team.value if hasattr(team, 'value') else str(team)
                if team_key not in team_tasks:
                    team_tasks[team_key] = {"total": 0, "completed": 0}
                
                for task in step["tasks"]:
                    team_tasks[team_key]["total"] += 1
                    if task["status"] == WorkflowStatus.COMPLETED.value:
                        team_tasks[team_key]["completed"] += 1
        
        report["team_summary"] = team_tasks
        report["notes"] = workflow["notes"]
        
        return report


# Example usage and testing functions
def create_sample_workflow():
    """Create a sample workflow for testing purposes."""
    workflow = EnhancedOffboardingWorkflow()
    
    # Sample employee data
    employee_data = {
        "employee_id": "EMP001",
        "name": "John Doe",
        "email": "john.doe@company.com",
        "last_working_day": "2024-02-15",
        "reason_for_leaving": ReasonForLeaving.RESIGNATION.value,
        "line_manager": "Jane Smith",
        "department": "Engineering",
        "position": "Senior Software Engineer"
    }
    
    # Create workflow
    request_id = workflow.create_offboarding_request(employee_data)
    
    print(f"Created workflow with request ID: {request_id}")
    
    # Get workflow status
    status = workflow.get_workflow_status(request_id)
    print(f"Workflow status: {status['status']}")
    print(f"Overall progress: {status['overall_progress']}%")
    
    return workflow, request_id


if __name__ == "__main__":
    # Run sample workflow
    workflow, request_id = create_sample_workflow()
    
    # Get tasks for different teams
    hr_tasks = workflow.get_tasks_by_team(TeamResponsibility.HR)
    it_tasks = workflow.get_tasks_by_team(TeamResponsibility.IT)
    
    print(f"\nHR Tasks: {len(hr_tasks)}")
    print(f"IT Tasks: {len(it_tasks)}")
    
    # Get overdue tasks
    overdue = workflow.get_overdue_tasks()
    print(f"\nOverdue tasks: {len(overdue)}") 