<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class ManagerModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Manager")

    def update_actions(self):
        """Update Manager-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Manager offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Confirm Handover
        handover_btn = self.create_action_button(
            "Confirm Handover",
            self.confirm_handover
        )
        handover_btn.pack(fill=tk.X, padx=5, pady=2)

        # Approve Exit Checklist
        exit_btn = self.create_action_button(
            "Approve Exit Checklist",
            self.approve_exit_checklist
        )
        exit_btn.pack(fill=tk.X, padx=5, pady=2)

    def confirm_handover(self):
        """Confirm work handover from the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for handover confirmation
        dialog = tk.Toplevel(self)
        dialog.title("Confirm Handover")
        dialog.geometry("500x500")

        # Handover information
        ttk.Label(dialog, text="Work Handover Details", font=("", 10, "bold")).pack(pady=10)

        # Handover items
        items = [
            "Project Documentation",
            "Code Repository Access",
            "Client Information",
            "Project Files",
            "Team Knowledge Transfer",
            "Pending Tasks",
            "Meeting Notes",
            "Training Materials"
        ]

        # Create checkboxes for each item
        checkboxes = {}
        for item in items:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=item,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[item] = var

        # Handover date
        ttk.Label(dialog, text="Handover Date:").pack(anchor=tk.W, padx=20)
        handover_date = ttk.Entry(dialog)
        handover_date.pack(fill=tk.X, padx=20, pady=5)
        handover_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Notes
        ttk.Label(dialog, text="Notes:").pack(anchor=tk.W, padx=20)
        notes = tk.Text(dialog, height=4, width=40)
        notes.pack(padx=20, pady=5)

        def process_handover():
            # Get selected items
            handed_over = [item for item, var in checkboxes.items() if var.get()]
            
            if not handed_over:
                self.show_error("Error", "Please select at least one item")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "handover_items": handed_over,
                    "handover_date": handover_date.get(),
                    "handover_notes": notes.get("1.0", tk.END).strip()
                }
            )

            self.show_message(
                "Success",
                f"Work handover confirmed for {self.selected_employee['name']}\n" +
                "Handed over items:\n" +
                "\n".join(f"- {item}" for item in handed_over)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Confirm Handover",
            command=process_handover
        ).pack(pady=20)

    def approve_exit_checklist(self):
        """Approve the employee's exit checklist."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for exit checklist approval
        dialog = tk.Toplevel(self)
        dialog.title("Approve Exit Checklist")
        dialog.geometry("500x400")

        # Exit checklist information
        ttk.Label(dialog, text="Exit Checklist Approval", font=("", 10, "bold")).pack(pady=10)

        # Checklist items
        items = [
            "All work handovers completed",
            "No pending tasks",
            "Knowledge transfer done",
            "Team informed about departure",
            "Client communications completed",
            "Project documentation updated",
            "Access rights revoked",
            "Company assets returned"
        ]

        # Create checkboxes for each item
        checkboxes = {}
        for item in items:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=item,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[item] = var

        # Approval date
        ttk.Label(dialog, text="Approval Date:").pack(anchor=tk.W, padx=20)
        approval_date = ttk.Entry(dialog)
        approval_date.pack(fill=tk.X, padx=20, pady=5)
        approval_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def process_approval():
            # Get selected items
            approved = [item for item, var in checkboxes.items() if var.get()]
            
            if not approved:
                self.show_error("Error", "Please select at least one item")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "exit_checklist_approved": approved,
                    "exit_approval_date": approval_date.get()
                }
            )

            self.show_message(
                "Success",
                f"Exit checklist approved for {self.selected_employee['name']}\n" +
                "Approved items:\n" +
                "\n".join(f"- {item}" for item in approved)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Approve Checklist",
            command=process_approval
=======
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class ManagerModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Manager")

    def update_actions(self):
        """Update Manager-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Manager offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Confirm Handover
        handover_btn = self.create_action_button(
            "Confirm Handover",
            self.confirm_handover
        )
        handover_btn.pack(fill=tk.X, padx=5, pady=2)

        # Approve Exit Checklist
        exit_btn = self.create_action_button(
            "Approve Exit Checklist",
            self.approve_exit_checklist
        )
        exit_btn.pack(fill=tk.X, padx=5, pady=2)

    def confirm_handover(self):
        """Confirm work handover from the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for handover confirmation
        dialog = tk.Toplevel(self)
        dialog.title("Confirm Handover")
        dialog.geometry("500x500")

        # Handover information
        ttk.Label(dialog, text="Work Handover Details", font=("", 10, "bold")).pack(pady=10)

        # Handover items
        items = [
            "Project Documentation",
            "Code Repository Access",
            "Client Information",
            "Project Files",
            "Team Knowledge Transfer",
            "Pending Tasks",
            "Meeting Notes",
            "Training Materials"
        ]

        # Create checkboxes for each item
        checkboxes = {}
        for item in items:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=item,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[item] = var

        # Handover date
        ttk.Label(dialog, text="Handover Date:").pack(anchor=tk.W, padx=20)
        handover_date = ttk.Entry(dialog)
        handover_date.pack(fill=tk.X, padx=20, pady=5)
        handover_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Notes
        ttk.Label(dialog, text="Notes:").pack(anchor=tk.W, padx=20)
        notes = tk.Text(dialog, height=4, width=40)
        notes.pack(padx=20, pady=5)

        def process_handover():
            # Get selected items
            handed_over = [item for item, var in checkboxes.items() if var.get()]
            
            if not handed_over:
                self.show_error("Error", "Please select at least one item")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "handover_items": handed_over,
                    "handover_date": handover_date.get(),
                    "handover_notes": notes.get("1.0", tk.END).strip()
                }
            )

            self.show_message(
                "Success",
                f"Work handover confirmed for {self.selected_employee['name']}\n" +
                "Handed over items:\n" +
                "\n".join(f"- {item}" for item in handed_over)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Confirm Handover",
            command=process_handover
        ).pack(pady=20)

    def approve_exit_checklist(self):
        """Approve the employee's exit checklist."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for exit checklist approval
        dialog = tk.Toplevel(self)
        dialog.title("Approve Exit Checklist")
        dialog.geometry("500x400")

        # Exit checklist information
        ttk.Label(dialog, text="Exit Checklist Approval", font=("", 10, "bold")).pack(pady=10)

        # Checklist items
        items = [
            "All work handovers completed",
            "No pending tasks",
            "Knowledge transfer done",
            "Team informed about departure",
            "Client communications completed",
            "Project documentation updated",
            "Access rights revoked",
            "Company assets returned"
        ]

        # Create checkboxes for each item
        checkboxes = {}
        for item in items:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=item,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[item] = var

        # Approval date
        ttk.Label(dialog, text="Approval Date:").pack(anchor=tk.W, padx=20)
        approval_date = ttk.Entry(dialog)
        approval_date.pack(fill=tk.X, padx=20, pady=5)
        approval_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def process_approval():
            # Get selected items
            approved = [item for item, var in checkboxes.items() if var.get()]
            
            if not approved:
                self.show_error("Error", "Please select at least one item")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "exit_checklist_approved": approved,
                    "exit_approval_date": approval_date.get()
                }
            )

            self.show_message(
                "Success",
                f"Exit checklist approved for {self.selected_employee['name']}\n" +
                "Approved items:\n" +
                "\n".join(f"- {item}" for item in approved)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Approve Checklist",
            command=process_approval
>>>>>>> 43451fc5cf1ae2c38def63e77b6905481892c38f
        ).pack(pady=20) 