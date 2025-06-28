import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class HRModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "HR")

    def update_actions(self):
        """Update HR-specific actions."""
        if not self.selected_employee:
            return

        # Submit resignation letter
        submit_btn = self.create_action_button(
            "Submit Resignation Letter",
            self.submit_resignation_letter
        )
        submit_btn.pack(fill=tk.X, padx=5, pady=2)

        # Status change frame
        status_frame = ttk.LabelFrame(self.actions_frame, text="Change Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        # Status dropdown
        self.status_var = tk.StringVar(value=self.selected_employee.get("status", "Active"))
        status_dropdown = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=["Active", "Resigned"],
            state="readonly"
        )
        status_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        # Update status button
        update_status_btn = ttk.Button(
            status_frame,
            text="Update Status",
            command=self.change_status
        )
        update_status_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Schedule exit interview
        interview_btn = self.create_action_button(
            "Schedule Exit Interview",
            self.schedule_exit_interview
        )
        interview_btn.pack(fill=tk.X, padx=5, pady=2)

        # Start offboarding process button
        if self.selected_employee["status"] == "Resigned":
            start_btn = self.create_action_button(
                "Start Offboarding Process",
                self.start_offboarding
            )
            start_btn.pack(fill=tk.X, padx=5, pady=2)

    def submit_resignation_letter(self):
        """Handle resignation letter submission."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        file_path = filedialog.askopenfilename(
            title="Select Resignation Letter",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if file_path:
            # In a real application, you would copy the file to a secure location
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {"resignation_letter": file_path}
            )
            self.show_message(
                "Success",
                f"Resignation letter submitted for {self.selected_employee['name']}"
            )
            self.update_details()
            self.update_progress()

    def change_status(self):
        """Change employee status."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        new_status = self.status_var.get()
        if new_status == self.selected_employee["status"]:
            self.show_error("Error", f"Employee is already {new_status}")
            return

        update_data = {"status": new_status}
        
        # If changing to Resigned, set exit date
        if new_status == "Resigned":
            update_data["exit_date"] = datetime.now().strftime("%Y-%m-%d")
        # If changing to Active, clear exit date
        elif new_status == "Active":
            update_data["exit_date"] = ""

        self.json_handler.update_employee(
            self.selected_employee["employee_id"],
            update_data
        )
        self.show_message(
            "Success",
            f"Status updated to {new_status} for {self.selected_employee['name']}"
        )
        self.update_details()
        self.update_actions()

    def schedule_exit_interview(self):
        """Schedule an exit interview."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for scheduling
        dialog = tk.Toplevel(self)
        dialog.title("Schedule Exit Interview")
        dialog.geometry("300x150")

        # Date selection
        ttk.Label(dialog, text="Interview Date:").pack(pady=5)
        date_entry = ttk.Entry(dialog)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Time selection
        ttk.Label(dialog, text="Interview Time:").pack(pady=5)
        time_entry = ttk.Entry(dialog)
        time_entry.pack(pady=5)
        time_entry.insert(0, "10:00")

        def save_schedule():
            date = date_entry.get()
            time = time_entry.get()
            # In a real application, you would save this to a calendar system
            self.show_message(
                "Success",
                f"Exit interview scheduled for {self.selected_employee['name']} on {date} at {time}"
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(dialog, text="Schedule", command=save_schedule).pack(pady=10)

    def start_offboarding(self):
        """Start the offboarding process for all departments."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        if self.selected_employee["status"] != "Resigned":
            self.show_error("Error", "Employee must be marked as Resigned to start offboarding")
            return

        # Initialize offboarding tracking
        tracking_data = self.offboarding_tracker.initialize_employee_tracking(
            self.selected_employee["employee_id"]
        )

        self.show_message(
            "Success",
            f"Offboarding process started for {self.selected_employee['name']}. All departments have been notified."
        )
        self.update_progress() 