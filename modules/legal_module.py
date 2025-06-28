<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class LegalModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Legal")

    def update_actions(self):
        """Update Legal-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Legal offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # NDA Status Check
        nda_btn = self.create_action_button(
            "Check NDA Status",
            self.check_nda_status
        )
        nda_btn.pack(fill=tk.X, padx=5, pady=2)

        # Document Return
        docs_btn = self.create_action_button(
            "Process Document Return",
            self.process_document_return
        )
        docs_btn.pack(fill=tk.X, padx=5, pady=2)

        # Dispute Resolution
        dispute_btn = self.create_action_button(
            "Handle Disputes",
            self.handle_disputes
        )
        dispute_btn.pack(fill=tk.X, padx=5, pady=2)

    def check_nda_status(self):
        """Check and update NDA status."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for NDA check
        dialog = tk.Toplevel(self)
        dialog.title("Check NDA Status")
        dialog.geometry("400x300")

        # NDA information
        ttk.Label(dialog, text="NDA Information", font=("", 10, "bold")).pack(pady=10)

        # NDA status
        ttk.Label(dialog, text="NDA Status:").pack(anchor=tk.W, padx=20)
        nda_status = ttk.Combobox(
            dialog,
            values=["Valid", "Expired", "Not Signed"],
            state="readonly"
        )
        nda_status.pack(fill=tk.X, padx=20, pady=5)
        nda_status.set(self.selected_employee.get("nda_status", "Not Signed"))

        # Expiry date
        ttk.Label(dialog, text="Expiry Date:").pack(anchor=tk.W, padx=20)
        expiry_date = ttk.Entry(dialog)
        expiry_date.pack(fill=tk.X, padx=20, pady=5)
        expiry_date.insert(0, self.selected_employee.get("nda_expiry", ""))

        def update_nda():
            status = nda_status.get()
            expiry = expiry_date.get()
            
            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "nda_status": status,
                    "nda_expiry": expiry
                }
            )

            self.show_message(
                "Success",
                f"NDA status updated for {self.selected_employee['name']}\n" +
                f"Status: {status}\n" +
                f"Expiry: {expiry}"
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Update NDA Status",
            command=update_nda
        ).pack(pady=20)

    def process_document_return(self):
        """Process return of legal documents."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for document return
        dialog = tk.Toplevel(self)
        dialog.title("Process Document Return")
        dialog.geometry("400x400")

        # Document information
        ttk.Label(dialog, text="Document Return Details", font=("", 10, "bold")).pack(pady=10)

        # Documents to return
        documents = [
            "Company ID Card",
            "Access Cards",
            "Confidential Documents",
            "Training Materials",
            "Company Property"
        ]

        # Create checkboxes for each document
        checkboxes = {}
        for doc in documents:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=doc,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[doc] = var

        # Return date
        ttk.Label(dialog, text="Return Date:").pack(anchor=tk.W, padx=20)
        return_date = ttk.Entry(dialog)
        return_date.pack(fill=tk.X, padx=20, pady=5)
        return_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def process_return():
            # Get selected documents
            returned = [doc for doc, var in checkboxes.items() if var.get()]
            
            if not returned:
                self.show_error("Error", "Please select at least one document")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "documents_returned": returned,
                    "document_return_date": return_date.get()
                }
            )

            self.show_message(
                "Success",
                f"Documents processed for {self.selected_employee['name']}\n" +
                "Returned items:\n" +
                "\n".join(f"- {doc}" for doc in returned)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Process Return",
            command=process_return
        ).pack(pady=20)

    def handle_disputes(self):
        """Handle any legal disputes."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for dispute handling
        dialog = tk.Toplevel(self)
        dialog.title("Handle Disputes")
        dialog.geometry("500x400")

        # Dispute information
        ttk.Label(dialog, text="Dispute Information", font=("", 10, "bold")).pack(pady=10)

        # Dispute type
        ttk.Label(dialog, text="Dispute Type:").pack(anchor=tk.W, padx=20)
        dispute_type = ttk.Combobox(
            dialog,
            values=[
                "None",
                "Contract Dispute",
                "Intellectual Property",
                "Non-Compete",
                "Confidentiality",
                "Other"
            ],
            state="readonly"
        )
        dispute_type.pack(fill=tk.X, padx=20, pady=5)
        dispute_type.set("None")

        # Dispute description
        ttk.Label(dialog, text="Description:").pack(anchor=tk.W, padx=20)
        description = tk.Text(dialog, height=4, width=40)
        description.pack(padx=20, pady=5)

        # Resolution status
        ttk.Label(dialog, text="Resolution Status:").pack(anchor=tk.W, padx=20)
        resolution = ttk.Combobox(
            dialog,
            values=["Pending", "In Progress", "Resolved", "Escalated"],
            state="readonly"
        )
        resolution.pack(fill=tk.X, padx=20, pady=5)
        resolution.set("Pending")

        def update_dispute():
            if dispute_type.get() == "None":
                # Clear dispute information
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "dispute_type": None,
                        "dispute_description": None,
                        "dispute_resolution": None
                    }
                )
            else:
                # Update dispute information
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "dispute_type": dispute_type.get(),
                        "dispute_description": description.get("1.0", tk.END).strip(),
                        "dispute_resolution": resolution.get()
                    }
                )

            self.show_message(
                "Success",
                f"Dispute information updated for {self.selected_employee['name']}\n" +
                f"Type: {dispute_type.get()}\n" +
                f"Status: {resolution.get()}"
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Update Dispute",
            command=update_dispute
=======
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class LegalModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Legal")

    def update_actions(self):
        """Update Legal-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Legal offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # NDA Status Check
        nda_btn = self.create_action_button(
            "Check NDA Status",
            self.check_nda_status
        )
        nda_btn.pack(fill=tk.X, padx=5, pady=2)

        # Document Return
        docs_btn = self.create_action_button(
            "Process Document Return",
            self.process_document_return
        )
        docs_btn.pack(fill=tk.X, padx=5, pady=2)

        # Dispute Resolution
        dispute_btn = self.create_action_button(
            "Handle Disputes",
            self.handle_disputes
        )
        dispute_btn.pack(fill=tk.X, padx=5, pady=2)

    def check_nda_status(self):
        """Check and update NDA status."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for NDA check
        dialog = tk.Toplevel(self)
        dialog.title("Check NDA Status")
        dialog.geometry("400x300")

        # NDA information
        ttk.Label(dialog, text="NDA Information", font=("", 10, "bold")).pack(pady=10)

        # NDA status
        ttk.Label(dialog, text="NDA Status:").pack(anchor=tk.W, padx=20)
        nda_status = ttk.Combobox(
            dialog,
            values=["Valid", "Expired", "Not Signed"],
            state="readonly"
        )
        nda_status.pack(fill=tk.X, padx=20, pady=5)
        nda_status.set(self.selected_employee.get("nda_status", "Not Signed"))

        # Expiry date
        ttk.Label(dialog, text="Expiry Date:").pack(anchor=tk.W, padx=20)
        expiry_date = ttk.Entry(dialog)
        expiry_date.pack(fill=tk.X, padx=20, pady=5)
        expiry_date.insert(0, self.selected_employee.get("nda_expiry", ""))

        def update_nda():
            status = nda_status.get()
            expiry = expiry_date.get()
            
            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "nda_status": status,
                    "nda_expiry": expiry
                }
            )

            self.show_message(
                "Success",
                f"NDA status updated for {self.selected_employee['name']}\n" +
                f"Status: {status}\n" +
                f"Expiry: {expiry}"
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Update NDA Status",
            command=update_nda
        ).pack(pady=20)

    def process_document_return(self):
        """Process return of legal documents."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for document return
        dialog = tk.Toplevel(self)
        dialog.title("Process Document Return")
        dialog.geometry("400x400")

        # Document information
        ttk.Label(dialog, text="Document Return Details", font=("", 10, "bold")).pack(pady=10)

        # Documents to return
        documents = [
            "Company ID Card",
            "Access Cards",
            "Confidential Documents",
            "Training Materials",
            "Company Property"
        ]

        # Create checkboxes for each document
        checkboxes = {}
        for doc in documents:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                dialog,
                text=doc,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=5)
            checkboxes[doc] = var

        # Return date
        ttk.Label(dialog, text="Return Date:").pack(anchor=tk.W, padx=20)
        return_date = ttk.Entry(dialog)
        return_date.pack(fill=tk.X, padx=20, pady=5)
        return_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def process_return():
            # Get selected documents
            returned = [doc for doc, var in checkboxes.items() if var.get()]
            
            if not returned:
                self.show_error("Error", "Please select at least one document")
                return

            # Update employee data
            self.json_handler.update_employee(
                self.selected_employee["employee_id"],
                {
                    "documents_returned": returned,
                    "document_return_date": return_date.get()
                }
            )

            self.show_message(
                "Success",
                f"Documents processed for {self.selected_employee['name']}\n" +
                "Returned items:\n" +
                "\n".join(f"- {doc}" for doc in returned)
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Process Return",
            command=process_return
        ).pack(pady=20)

    def handle_disputes(self):
        """Handle any legal disputes."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for dispute handling
        dialog = tk.Toplevel(self)
        dialog.title("Handle Disputes")
        dialog.geometry("500x400")

        # Dispute information
        ttk.Label(dialog, text="Dispute Information", font=("", 10, "bold")).pack(pady=10)

        # Dispute type
        ttk.Label(dialog, text="Dispute Type:").pack(anchor=tk.W, padx=20)
        dispute_type = ttk.Combobox(
            dialog,
            values=[
                "None",
                "Contract Dispute",
                "Intellectual Property",
                "Non-Compete",
                "Confidentiality",
                "Other"
            ],
            state="readonly"
        )
        dispute_type.pack(fill=tk.X, padx=20, pady=5)
        dispute_type.set("None")

        # Dispute description
        ttk.Label(dialog, text="Description:").pack(anchor=tk.W, padx=20)
        description = tk.Text(dialog, height=4, width=40)
        description.pack(padx=20, pady=5)

        # Resolution status
        ttk.Label(dialog, text="Resolution Status:").pack(anchor=tk.W, padx=20)
        resolution = ttk.Combobox(
            dialog,
            values=["Pending", "In Progress", "Resolved", "Escalated"],
            state="readonly"
        )
        resolution.pack(fill=tk.X, padx=20, pady=5)
        resolution.set("Pending")

        def update_dispute():
            if dispute_type.get() == "None":
                # Clear dispute information
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "dispute_type": None,
                        "dispute_description": None,
                        "dispute_resolution": None
                    }
                )
            else:
                # Update dispute information
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "dispute_type": dispute_type.get(),
                        "dispute_description": description.get("1.0", tk.END).strip(),
                        "dispute_resolution": resolution.get()
                    }
                )

            self.show_message(
                "Success",
                f"Dispute information updated for {self.selected_employee['name']}\n" +
                f"Type: {dispute_type.get()}\n" +
                f"Status: {resolution.get()}"
            )
            dialog.destroy()
            self.update_progress()
            self.update_details()

        ttk.Button(
            dialog,
            text="Update Dispute",
            command=update_dispute
>>>>>>> 43451fc5cf1ae2c38def63e77b6905481892c38f
        ).pack(pady=20) 