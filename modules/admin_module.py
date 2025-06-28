import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class AdminModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Admin")

    def update_actions(self):
        """Update Admin-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Admin offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Reclaim Access Cards/Keys
        access_btn = self.create_action_button(
            "Reclaim Access Cards/Keys",
            self.reclaim_access
        )
        access_btn.pack(fill=tk.X, padx=5, pady=2)

        # Facility Clearance
        facility_btn = self.create_action_button(
            "Process Facility Clearance",
            self.process_facility_clearance
        )
        facility_btn.pack(fill=tk.X, padx=5, pady=2)

    def reclaim_access(self):
        """Process return of access cards and keys."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for access card/key return
        dialog = tk.Toplevel(self)
        dialog.title("Reclaim Access Cards/Keys")
        dialog.geometry("400x400")

        # Access items information
        ttk.Label(dialog, text="Access Items Return", font=("", 10, "bold")).pack(pady=10)

        # Items to return
        items = [
            "Office Access Card",
            "Building Access Card",
            "Parking Access Card",
            "Office Keys",
            "Locker Keys",
            "Cabinet Keys"
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

        # Return date
        ttk.Label(dialog, text="Return Date:").pack(anchor=tk.W, padx=20)
        return_date = ttk.Entry(dialog)
        return_date.pack(fill=tk.X, padx=20, pady=5)
        return_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def process_return():
            # Get selected items
            returned = [item for item, var in checkboxes.items() if var.get()]
            
            if not returned:
                self.show_error("Error", "Please select at least one item")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "access_items_returned": returned,
                    "access_return_date": return_date.get()
                }
            )

            self.show_message(
                "Success",
                f"Access items processed for {self.selected_employee['name']}\n" +
                "Returned items:\n" +
                "\n".join(f"- {item}" for item in returned)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Process Return",
            command=process_return
        ).pack(pady=20)

    def process_facility_clearance(self):
        """Process facility clearance for the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for facility clearance
        dialog = tk.Toplevel(self)
        dialog.title("Process Facility Clearance")
        dialog.geometry("500x400")

        # Facility clearance information
        ttk.Label(dialog, text="Facility Clearance Details", font=("", 10, "bold")).pack(pady=10)

        # Areas to clear
        areas = [
            "Workstation",
            "Office Locker",
            "Parking Space",
            "Company Vehicle",
            "Storage Area",
            "Common Areas"
        ]

        # Create checkboxes for each area
        checkboxes = {}
        for area in areas:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=area,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[area] = var

        # Clearance date
        ttk.Label(dialog, text="Clearance Date:").pack(anchor=tk.W, padx=20)
        clearance_date = ttk.Entry(dialog)
        clearance_date.pack(fill=tk.X, padx=20, pady=5)
        clearance_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Notes
        ttk.Label(dialog, text="Notes:").pack(anchor=tk.W, padx=20)
        notes = tk.Text(dialog, height=4, width=40)
        notes.pack(padx=20, pady=5)

        def process_clearance():
            # Get selected areas
            cleared = [area for area, var in checkboxes.items() if var.get()]
            
            if not cleared:
                self.show_error("Error", "Please select at least one area")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "facility_areas_cleared": cleared,
                    "facility_clearance_date": clearance_date.get(),
                    "facility_clearance_notes": notes.get("1.0", tk.END).strip()
                }
            )

            self.show_message(
                "Success",
                f"Facility clearance processed for {self.selected_employee['name']}\n" +
                "Cleared areas:\n" +
                "\n".join(f"- {area}" for area in cleared)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Process Clearance",
            command=process_clearance
        ).pack(pady=20) 