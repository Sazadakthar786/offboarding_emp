import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class ITModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "IT")

    def update_actions(self):
        """Update IT-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform IT offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Revoke System Access
        revoke_btn = self.create_action_button(
            "Revoke System Access",
            self.revoke_system_access
        )
        revoke_btn.pack(fill=tk.X, padx=5, pady=2)

        # Return Company Device
        device_btn = self.create_action_button(
            "Process Device Return",
            self.process_device_return
        )
        device_btn.pack(fill=tk.X, padx=5, pady=2)

        # Backup Files
        backup_btn = self.create_action_button(
            "Backup Employee Files",
            self.backup_employee_files
        )
        backup_btn.pack(fill=tk.X, padx=5, pady=2)

    def revoke_system_access(self):
        """Handle system access revocation."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for access revocation
        dialog = tk.Toplevel(self)
        dialog.title("Revoke System Access")
        dialog.geometry("400x300")

        # Systems to revoke access from
        systems = [
            "Email Account",
            "VPN Access",
            "Internal Systems",
            "Cloud Services",
            "Development Tools",
            "Project Management Tools"
        ]

        # Create checkboxes for each system
        checkboxes = {}
        for i, system in enumerate(systems):
            var = tk.BooleanVar(value=True)
            ttk.Checkbutton(
                dialog,
                text=system,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[system] = var

        def confirm_revocation():
            # Get selected systems
            selected = [sys for sys, var in checkboxes.items() if var.get()]
            
            if not selected:
                self.show_error("Error", "Please select at least one system")
                return

            # In a real application, you would revoke access to these systems
            self.show_message(
                "Success",
                f"Access revoked for {self.selected_employee['name']} from:\n" + 
                "\n".join(f"- {sys}" for sys in selected)
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(
            dialog,
            text="Confirm Revocation",
            command=confirm_revocation
        ).pack(pady=20)

    def process_device_return(self):
        """Handle company device return process."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for device return
        dialog = tk.Toplevel(self)
        dialog.title("Process Device Return")
        dialog.geometry("400x350")

        # Device information
        ttk.Label(dialog, text="Device Information", font=("", 10, "bold")).pack(pady=10)

        # Device type
        ttk.Label(dialog, text="Device Type:").pack(anchor=tk.W, padx=20)
        device_type = ttk.Combobox(
            dialog,
            values=["Laptop", "Desktop", "Mobile Phone", "Tablet", "Other"],
            state="readonly"
        )
        device_type.pack(fill=tk.X, padx=20, pady=5)

        # Device condition
        ttk.Label(dialog, text="Device Condition:").pack(anchor=tk.W, padx=20)
        condition = ttk.Combobox(
            dialog,
            values=["Good", "Minor Damage", "Major Damage", "Not Working"],
            state="readonly"
        )
        condition.pack(fill=tk.X, padx=20, pady=5)

        # Additional notes
        ttk.Label(dialog, text="Additional Notes:").pack(anchor=tk.W, padx=20)
        notes = tk.Text(dialog, height=4, width=40)
        notes.pack(padx=20, pady=5)

        def confirm_return():
            if not device_type.get():
                self.show_error("Error", "Please select device type")
                return
            if not condition.get():
                self.show_error("Error", "Please select device condition")
                return

            # In a real application, you would record this information
            self.show_message(
                "Success",
                f"Device return processed for {self.selected_employee['name']}\n" +
                f"Device: {device_type.get()}\n" +
                f"Condition: {condition.get()}"
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(
            dialog,
            text="Confirm Return",
            command=confirm_return
        ).pack(pady=20)

    def backup_employee_files(self):
        """Handle employee file backup process."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for file backup
        dialog = tk.Toplevel(self)
        dialog.title("Backup Employee Files")
        dialog.geometry("400x300")

        # Backup options
        ttk.Label(dialog, text="Select Files to Backup", font=("", 10, "bold")).pack(pady=10)

        # File locations to backup
        locations = [
            "Local Drive",
            "Network Drive",
            "Cloud Storage",
            "Email Attachments",
            "Project Repositories"
        ]

        # Create checkboxes for each location
        checkboxes = {}
        for i, location in enumerate(locations):
            var = tk.BooleanVar(value=True)
            ttk.Checkbutton(
                dialog,
                text=location,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[location] = var

        def start_backup():
            # Get selected locations
            selected = [loc for loc, var in checkboxes.items() if var.get()]
            
            if not selected:
                self.show_error("Error", "Please select at least one location")
                return

            # In a real application, you would perform the backup
            self.show_message(
                "Success",
                f"Backup initiated for {self.selected_employee['name']} from:\n" + 
                "\n".join(f"- {loc}" for loc in selected)
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(
            dialog,
            text="Start Backup",
            command=start_backup
        ).pack(pady=20) 