import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable
from utils.json_handler import JSONHandler
from utils.offboarding_tracker import OffboardingTracker

class BaseModule(ttk.Frame):
    def __init__(self, parent, json_handler: JSONHandler, department: str):
        super().__init__(parent)
        self.json_handler = json_handler
        self.department = department
        self.selected_employee = None
        self.offboarding_tracker = OffboardingTracker()
        self.setup_ui()

    def setup_ui(self):
        """Setup the basic UI components."""
        # Employee selection frame
        selection_frame = ttk.LabelFrame(self, text="Select Employee")
        selection_frame.pack(fill=tk.X, padx=5, pady=5)

        # Employee dropdown
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.employee_var,
            state="readonly"
        )
        self.employee_dropdown.pack(fill=tk.X, padx=5, pady=5)
        self.update_employee_list()
        self.employee_dropdown.bind('<<ComboboxSelected>>', self.on_employee_select)

        # Employee details frame
        self.details_frame = ttk.LabelFrame(self, text="Employee Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Offboarding progress frame
        self.progress_frame = ttk.LabelFrame(self, text="Offboarding Progress")
        self.progress_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Actions frame
        self.actions_frame = ttk.LabelFrame(self, text="Department Actions")
        self.actions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_employee_list(self):
        """Update the employee dropdown list."""
        employees = self.json_handler.get_all_employees()
        self.employee_dropdown['values'] = [
            f"{emp['name']} ({emp['employee_id']})" for emp in employees
        ]

    def on_employee_select(self, event):
        """Handle employee selection from dropdown."""
        selection = self.employee_var.get()
        if selection:
            employee_id = selection.split('(')[-1].strip(')')
            self.selected_employee = self.json_handler.get_employee_by_id(employee_id)
            self.update_details()
            self.update_progress()
            self.update_actions()

    def update_details(self):
        """Update employee details display."""
        # Clear existing widgets
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        if not self.selected_employee:
            return

        # Create details display
        row = 0
        for key, value in self.selected_employee.items():
            ttk.Label(self.details_frame, text=f"{key.replace('_', ' ').title()}:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            ttk.Label(self.details_frame, text=str(value)).grid(
                row=row, column=1, sticky=tk.W, padx=5, pady=2
            )
            row += 1

    def update_progress(self):
        """Update the offboarding progress display."""
        # Clear existing widgets
        for widget in self.progress_frame.winfo_children():
            widget.destroy()

        if not self.selected_employee:
            return

        # Get department tasks
        dept_tasks = self.offboarding_tracker.departments[self.department]["tasks"]
        
        # Create progress display
        row = 0
        for task in dept_tasks:
            # Task label
            ttk.Label(self.progress_frame, text=task).grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            
            # Task status
            status_var = tk.StringVar(value="Pending")
            status_dropdown = ttk.Combobox(
                self.progress_frame,
                textvariable=status_var,
                values=["Pending", "In Progress", "Completed"],
                state="readonly",
                width=15
            )
            status_dropdown.grid(row=row, column=1, padx=5, pady=2)
            
            # Update button
            update_btn = ttk.Button(
                self.progress_frame,
                text="Update",
                command=lambda t=task, s=status_var: self.update_task_status(t, s.get())
            )
            update_btn.grid(row=row, column=2, padx=5, pady=2)
            
            row += 1

    def update_task_status(self, task: str, status: str):
        """Update the status of a task."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # In a real application, you would save this to a database
        self.show_message(
            "Success",
            f"Task '{task}' status updated to {status}"
        )
        self.update_progress()

    def update_actions(self):
        """Update department-specific actions."""
        # Clear existing widgets
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if not self.selected_employee:
            return

        # This method should be overridden by department-specific modules
        pass

    def create_action_button(self, text: str, command: Callable):
        """Create a standard action button."""
        return ttk.Button(
            self.actions_frame,
            text=text,
            command=command
        )

    def show_message(self, title: str, message: str):
        """Show a message dialog."""
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str):
        """Show an error dialog."""
        messagebox.showerror(title, message) 