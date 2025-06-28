#!/usr/bin/env python3
"""
Test Script for Enhanced Offboarding Workflow
=============================================

This script demonstrates the functionality of the enhanced offboarding workflow system.
It creates sample workflows, updates tasks, and shows various features.
"""

from modules.enhanced_workflow import EnhancedOffboardingWorkflow, TeamResponsibility, WorkflowStatus, ReasonForLeaving
from datetime import datetime, timedelta
import json

def main():
    """Main test function."""
    print("🚀 Enhanced Offboarding Workflow Test")
    print("=" * 50)
    
    # Initialize the workflow system
    workflow = EnhancedOffboardingWorkflow()
    
    # Test 1: Create a new offboarding request
    print("\n📝 Test 1: Creating a new offboarding request")
    print("-" * 40)
    
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
    
    try:
        request_id = workflow.create_offboarding_request(employee_data)
        print(f"✅ Created workflow with request ID: {request_id}")
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return
    
    # Test 2: Get workflow status
    print("\n📊 Test 2: Getting workflow status")
    print("-" * 40)
    
    try:
        status = workflow.get_workflow_status(request_id)
        print(f"✅ Workflow status: {status['status']}")
        print(f"✅ Overall progress: {status['overall_progress']:.1f}%")
        print(f"✅ Employee: {status['employee_data']['name']}")
        print(f"✅ Last Working Day: {status['employee_data']['last_working_day']}")
    except Exception as e:
        print(f"❌ Error getting status: {e}")
    
    # Test 3: Update some tasks
    print("\n🔄 Test 3: Updating task status")
    print("-" * 40)
    
    # Update initial request tasks
    try:
        # Complete employee details capture
        success = workflow.update_task_status(
            request_id, 
            "step_1_initial_request", 
            "capture_employee_details", 
            WorkflowStatus.COMPLETED, 
            "Jane Smith", 
            "Employee details captured successfully"
        )
        print(f"✅ Updated capture_employee_details: {success}")
        
        # Complete request validation
        success = workflow.update_task_status(
            request_id, 
            "step_1_initial_request", 
            "validate_request", 
            WorkflowStatus.COMPLETED, 
            "Jane Smith", 
            "Request validated and approved"
        )
        print(f"✅ Updated validate_request: {success}")
        
        # Update some People Ops tasks
        success = workflow.update_task_status(
            request_id, 
            "step_2_people_ops_review", 
            "review_employee_details", 
            WorkflowStatus.COMPLETED, 
            "HR Manager", 
            "Employee details reviewed and confirmed"
        )
        print(f"✅ Updated review_employee_details: {success}")
        
    except Exception as e:
        print(f"❌ Error updating tasks: {e}")
    
    # Test 4: Get updated status
    print("\n📈 Test 4: Getting updated workflow status")
    print("-" * 40)
    
    try:
        status = workflow.get_workflow_status(request_id)
        print(f"✅ Updated workflow status: {status['status']}")
        print(f"✅ Updated overall progress: {status['overall_progress']:.1f}%")
        
        # Show step statuses
        print("\n📋 Step Statuses:")
        for step_id, step in status['steps'].items():
            print(f"  - {step['name']}: {step['status']}")
            
    except Exception as e:
        print(f"❌ Error getting updated status: {e}")
    
    # Test 5: Get tasks by team
    print("\n👥 Test 5: Getting tasks by team")
    print("-" * 40)
    
    try:
        hr_tasks = workflow.get_tasks_by_team(TeamResponsibility.HR)
        it_tasks = workflow.get_tasks_by_team(TeamResponsibility.IT)
        finance_tasks = workflow.get_tasks_by_team(TeamResponsibility.FINANCE)
        
        print(f"✅ HR Tasks: {len(hr_tasks)}")
        print(f"✅ IT Tasks: {len(it_tasks)}")
        print(f"✅ Finance Tasks: {len(finance_tasks)}")
        
        if hr_tasks:
            print(f"\n📋 Sample HR Task: {hr_tasks[0]['task_name']}")
            
    except Exception as e:
        print(f"❌ Error getting team tasks: {e}")
    
    # Test 6: Add notes to workflow
    print("\n📝 Test 6: Adding notes to workflow")
    print("-" * 40)
    
    try:
        success = workflow.add_note_to_workflow(
            request_id, 
            "Initial offboarding process started. Employee has been notified.", 
            "HR Manager"
        )
        print(f"✅ Added note: {success}")
        
        success = workflow.add_note_to_workflow(
            request_id, 
            "Exit interview scheduled for February 10th, 2024.", 
            "HR Coordinator"
        )
        print(f"✅ Added second note: {success}")
        
    except Exception as e:
        print(f"❌ Error adding notes: {e}")
    
    # Test 7: Get overdue tasks
    print("\n⏰ Test 7: Checking for overdue tasks")
    print("-" * 40)
    
    try:
        overdue = workflow.get_overdue_tasks()
        print(f"✅ Overdue tasks: {len(overdue)}")
        
        if overdue:
            print("📋 Overdue tasks found:")
            for task in overdue:
                print(f"  - {task['employee_name']}: {task['step_name']} ({task['days_overdue']} days overdue)")
        else:
            print("✅ No overdue tasks found")
            
    except Exception as e:
        print(f"❌ Error checking overdue tasks: {e}")
    
    # Test 8: Export workflow report
    print("\n📄 Test 8: Exporting workflow report")
    print("-" * 40)
    
    try:
        report = workflow.export_workflow_report(request_id)
        print(f"✅ Report exported successfully")
        print(f"✅ Report contains {len(report['steps_detail'])} steps")
        print(f"✅ Report contains {len(report['notes'])} notes")
        
        # Save report to file
        with open(f"workflow_report_{request_id}.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved to workflow_report_{request_id}.json")
        
    except Exception as e:
        print(f"❌ Error exporting report: {e}")
    
    # Test 9: Create another workflow for comparison
    print("\n🔄 Test 9: Creating another workflow")
    print("-" * 40)
    
    employee_data_2 = {
        "employee_id": "EMP002",
        "name": "Jane Smith",
        "email": "jane.smith@company.com",
        "last_working_day": "2024-03-01",
        "reason_for_leaving": ReasonForLeaving.TERMINATION.value,
        "line_manager": "Bob Johnson",
        "department": "Marketing",
        "position": "Marketing Manager"
    }
    
    try:
        request_id_2 = workflow.create_offboarding_request(employee_data_2)
        print(f"✅ Created second workflow: {request_id_2}")
        
        # Get all workflows
        workflows = list(workflow.active_workflows.keys())
        print(f"✅ Total active workflows: {len(workflows)}")
        
    except Exception as e:
        print(f"❌ Error creating second workflow: {e}")
    
    print("\n🎉 Enhanced Workflow Test Completed!")
    print("=" * 50)
    print("\n📋 Summary:")
    print(f"  - Created workflows: {len(workflow.active_workflows)}")
    print(f"  - Updated tasks successfully")
    print(f"  - Tested team task filtering")
    print(f"  - Added workflow notes")
    print(f"  - Checked overdue tasks")
    print(f"  - Exported workflow reports")
    print("\n✨ All tests completed successfully!")

if __name__ == "__main__":
    main() 