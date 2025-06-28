<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class FinanceModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Finance")

    def update_actions(self):
        """Update Finance-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Finance offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Calculate Settlement
        settlement_btn = self.create_action_button(
            "Calculate Settlement",
            self.calculate_settlement
        )
        settlement_btn.pack(fill=tk.X, padx=5, pady=2)

        # Check Loans
        loans_btn = self.create_action_button(
            "Check Loans",
            self.check_loans
        )
        loans_btn.pack(fill=tk.X, padx=5, pady=2)

        # Generate Final Payslip
        payslip_btn = self.create_action_button(
            "Generate Final Payslip",
            self.generate_payslip
        )
        payslip_btn.pack(fill=tk.X, padx=5, pady=2)

    def calculate_settlement(self):
        """Calculate final settlement for the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for settlement calculation
        dialog = tk.Toplevel(self)
        dialog.title("Calculate Settlement")
        dialog.geometry("500x400")

        # Settlement components
        ttk.Label(dialog, text="Settlement Components", font=("", 10, "bold")).pack(pady=10)

        # Basic salary
        ttk.Label(dialog, text="Basic Salary:").pack(anchor=tk.W, padx=20)
        basic_salary = ttk.Entry(dialog)
        basic_salary.pack(fill=tk.X, padx=20, pady=5)
        basic_salary.insert(0, "0")

        # Allowances
        ttk.Label(dialog, text="Allowances:").pack(anchor=tk.W, padx=20)
        allowances = ttk.Entry(dialog)
        allowances.pack(fill=tk.X, padx=20, pady=5)
        allowances.insert(0, "0")

        # Benefits
        ttk.Label(dialog, text="Benefits:").pack(anchor=tk.W, padx=20)
        benefits = ttk.Entry(dialog)
        benefits.pack(fill=tk.X, padx=20, pady=5)
        benefits.insert(0, "0")

        # Deductions
        ttk.Label(dialog, text="Deductions:").pack(anchor=tk.W, padx=20)
        deductions = ttk.Entry(dialog)
        deductions.pack(fill=tk.X, padx=20, pady=5)
        deductions.insert(0, "0")

        def calculate():
            try:
                total = (
                    float(basic_salary.get()) +
                    float(allowances.get()) +
                    float(benefits.get()) -
                    float(deductions.get())
                )
                
                # Update employee data
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {"final_salary": total}
                )

                self.show_message(
                    "Success",
                    f"Settlement calculated for {self.selected_employee['name']}\n" +
                    f"Total Amount: ${total:,.2f}"
                )
                dialog.destroy()
                self.update_progress()
                self.update_details()
            except ValueError:
                self.show_error("Error", "Please enter valid numbers")

        ttk.Button(
            dialog,
            text="Calculate",
            command=calculate
        ).pack(pady=20)

    def check_loans(self):
        """Check and process employee loans."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for loan check
        dialog = tk.Toplevel(self)
        dialog.title("Check Loans")
        dialog.geometry("400x300")

        # Loan information
        ttk.Label(dialog, text="Loan Information", font=("", 10, "bold")).pack(pady=10)

        # Loan balance
        ttk.Label(dialog, text="Current Loan Balance:").pack(anchor=tk.W, padx=20)
        loan_balance = ttk.Entry(dialog)
        loan_balance.pack(fill=tk.X, padx=20, pady=5)
        loan_balance.insert(0, str(self.selected_employee.get("loan_balance", 0)))

        # Payment status
        ttk.Label(dialog, text="Payment Status:").pack(anchor=tk.W, padx=20)
        payment_status = ttk.Combobox(
            dialog,
            values=["Pending", "Partially Paid", "Fully Paid"],
            state="readonly"
        )
        payment_status.pack(fill=tk.X, padx=20, pady=5)
        payment_status.set("Pending" if self.selected_employee.get("loan_balance", 0) > 0 else "Fully Paid")

        def update_loan():
            try:
                balance = float(loan_balance.get())
                status = payment_status.get()
                
                # Update employee data
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "loan_balance": balance,
                        "paid_loan": status == "Fully Paid"
                    }
                )

                self.show_message(
                    "Success",
                    f"Loan status updated for {self.selected_employee['name']}\n" +
                    f"Balance: ${balance:,.2f}\n" +
                    f"Status: {status}"
                )
                dialog.destroy()
                self.update_progress()
                self.update_details()
            except ValueError:
                self.show_error("Error", "Please enter valid numbers")

        ttk.Button(
            dialog,
            text="Update Loan Status",
            command=update_loan
        ).pack(pady=20)

    def generate_payslip(self):
        """Generate final payslip for the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for payslip generation
        dialog = tk.Toplevel(self)
        dialog.title("Generate Final Payslip")
        dialog.geometry("400x300")

        # Payslip information
        ttk.Label(dialog, text="Payslip Details", font=("", 10, "bold")).pack(pady=10)

        # Payment date
        ttk.Label(dialog, text="Payment Date:").pack(anchor=tk.W, padx=20)
        payment_date = ttk.Entry(dialog)
        payment_date.pack(fill=tk.X, padx=20, pady=5)
        payment_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Payment method
        ttk.Label(dialog, text="Payment Method:").pack(anchor=tk.W, padx=20)
        payment_method = ttk.Combobox(
            dialog,
            values=["Bank Transfer", "Check", "Cash"],
            state="readonly"
        )
        payment_method.pack(fill=tk.X, padx=20, pady=5)
        payment_method.set("Bank Transfer")

        def generate():
            if not payment_date.get() or not payment_method.get():
                self.show_error("Error", "Please fill in all fields")
                return

            # In a real application, you would generate a PDF payslip
            self.show_message(
                "Success",
                f"Final payslip generated for {self.selected_employee['name']}\n" +
                f"Payment Date: {payment_date.get()}\n" +
                f"Payment Method: {payment_method.get()}\n" +
                f"Amount: ${self.selected_employee.get('final_salary', 0):,.2f}"
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(
            dialog,
            text="Generate Payslip",
            command=generate
=======
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from .base_module import BaseModule

class FinanceModule(BaseModule):
    def __init__(self, parent, json_handler):
        super().__init__(parent, json_handler, "Finance")

    def update_actions(self):
        """Update Finance-specific actions."""
        if not self.selected_employee:
            return

        # Only show actions if employee is resigned
        if self.selected_employee["status"] != "Resigned":
            ttk.Label(
                self.actions_frame,
                text="Employee must be marked as Resigned to perform Finance offboarding tasks",
                wraplength=300
            ).pack(padx=5, pady=5)
            return

        # Calculate Settlement
        settlement_btn = self.create_action_button(
            "Calculate Settlement",
            self.calculate_settlement
        )
        settlement_btn.pack(fill=tk.X, padx=5, pady=2)

        # Check Loans
        loans_btn = self.create_action_button(
            "Check Loans",
            self.check_loans
        )
        loans_btn.pack(fill=tk.X, padx=5, pady=2)

        # Generate Final Payslip
        payslip_btn = self.create_action_button(
            "Generate Final Payslip",
            self.generate_payslip
        )
        payslip_btn.pack(fill=tk.X, padx=5, pady=2)

    def calculate_settlement(self):
        """Calculate final settlement for the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for settlement calculation
        dialog = tk.Toplevel(self)
        dialog.title("Calculate Settlement")
        dialog.geometry("500x400")

        # Settlement components
        ttk.Label(dialog, text="Settlement Components", font=("", 10, "bold")).pack(pady=10)

        # Basic salary
        ttk.Label(dialog, text="Basic Salary:").pack(anchor=tk.W, padx=20)
        basic_salary = ttk.Entry(dialog)
        basic_salary.pack(fill=tk.X, padx=20, pady=5)
        basic_salary.insert(0, "0")

        # Allowances
        ttk.Label(dialog, text="Allowances:").pack(anchor=tk.W, padx=20)
        allowances = ttk.Entry(dialog)
        allowances.pack(fill=tk.X, padx=20, pady=5)
        allowances.insert(0, "0")

        # Benefits
        ttk.Label(dialog, text="Benefits:").pack(anchor=tk.W, padx=20)
        benefits = ttk.Entry(dialog)
        benefits.pack(fill=tk.X, padx=20, pady=5)
        benefits.insert(0, "0")

        # Deductions
        ttk.Label(dialog, text="Deductions:").pack(anchor=tk.W, padx=20)
        deductions = ttk.Entry(dialog)
        deductions.pack(fill=tk.X, padx=20, pady=5)
        deductions.insert(0, "0")

        def calculate():
            try:
                total = (
                    float(basic_salary.get()) +
                    float(allowances.get()) +
                    float(benefits.get()) -
                    float(deductions.get())
                )
                
                # Update employee data
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {"final_salary": total}
                )

                self.show_message(
                    "Success",
                    f"Settlement calculated for {self.selected_employee['name']}\n" +
                    f"Total Amount: ${total:,.2f}"
                )
                dialog.destroy()
                self.update_progress()
                self.update_details()
            except ValueError:
                self.show_error("Error", "Please enter valid numbers")

        ttk.Button(
            dialog,
            text="Calculate",
            command=calculate
        ).pack(pady=20)

    def check_loans(self):
        """Check and process employee loans."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for loan check
        dialog = tk.Toplevel(self)
        dialog.title("Check Loans")
        dialog.geometry("400x300")

        # Loan information
        ttk.Label(dialog, text="Loan Information", font=("", 10, "bold")).pack(pady=10)

        # Loan balance
        ttk.Label(dialog, text="Current Loan Balance:").pack(anchor=tk.W, padx=20)
        loan_balance = ttk.Entry(dialog)
        loan_balance.pack(fill=tk.X, padx=20, pady=5)
        loan_balance.insert(0, str(self.selected_employee.get("loan_balance", 0)))

        # Payment status
        ttk.Label(dialog, text="Payment Status:").pack(anchor=tk.W, padx=20)
        payment_status = ttk.Combobox(
            dialog,
            values=["Pending", "Partially Paid", "Fully Paid"],
            state="readonly"
        )
        payment_status.pack(fill=tk.X, padx=20, pady=5)
        payment_status.set("Pending" if self.selected_employee.get("loan_balance", 0) > 0 else "Fully Paid")

        def update_loan():
            try:
                balance = float(loan_balance.get())
                status = payment_status.get()
                
                # Update employee data
                self.json_handler.update_employee(
                    self.selected_employee["employee_id"],
                    {
                        "loan_balance": balance,
                        "paid_loan": status == "Fully Paid"
                    }
                )

                self.show_message(
                    "Success",
                    f"Loan status updated for {self.selected_employee['name']}\n" +
                    f"Balance: ${balance:,.2f}\n" +
                    f"Status: {status}"
                )
                dialog.destroy()
                self.update_progress()
                self.update_details()
            except ValueError:
                self.show_error("Error", "Please enter valid numbers")

        ttk.Button(
            dialog,
            text="Update Loan Status",
            command=update_loan
        ).pack(pady=20)

    def generate_payslip(self):
        """Generate final payslip for the employee."""
        if not self.selected_employee:
            self.show_error("Error", "No employee selected")
            return

        # Create a dialog for payslip generation
        dialog = tk.Toplevel(self)
        dialog.title("Generate Final Payslip")
        dialog.geometry("400x300")

        # Payslip information
        ttk.Label(dialog, text="Payslip Details", font=("", 10, "bold")).pack(pady=10)

        # Payment date
        ttk.Label(dialog, text="Payment Date:").pack(anchor=tk.W, padx=20)
        payment_date = ttk.Entry(dialog)
        payment_date.pack(fill=tk.X, padx=20, pady=5)
        payment_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Payment method
        ttk.Label(dialog, text="Payment Method:").pack(anchor=tk.W, padx=20)
        payment_method = ttk.Combobox(
            dialog,
            values=["Bank Transfer", "Check", "Cash"],
            state="readonly"
        )
        payment_method.pack(fill=tk.X, padx=20, pady=5)
        payment_method.set("Bank Transfer")

        def generate():
            if not payment_date.get() or not payment_method.get():
                self.show_error("Error", "Please fill in all fields")
                return

            # In a real application, you would generate a PDF payslip
            self.show_message(
                "Success",
                f"Final payslip generated for {self.selected_employee['name']}\n" +
                f"Payment Date: {payment_date.get()}\n" +
                f"Payment Method: {payment_method.get()}\n" +
                f"Amount: ${self.selected_employee.get('final_salary', 0):,.2f}"
            )
            dialog.destroy()
            self.update_progress()

        ttk.Button(
            dialog,
            text="Generate Payslip",
            command=generate
>>>>>>> 43451fc5cf1ae2c38def63e77b6905481892c38f
        ).pack(pady=20) 