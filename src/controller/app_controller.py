import csv
from fpdf import FPDF
from src.model.database import DatabaseManager
from src.model.ai_model import ExpenseCategorizerAI

class AppController:
    def __init__(self):
        self.db = DatabaseManager()
        self.ai = ExpenseCategorizerAI()
        
        # Train AI Model on startup
        try:
            self.ai.train()
        except Exception as e:
            print(f"Controller Error: Failed to initialize AI. {e}")

    def register(self, username, password):
        return self.db.register_user(username, password)

    def login(self, username, password):
        return self.db.authenticate_user(username, password)

    def add_single_transaction(self, user_id, t_type, date, description, amount, category=None):
        """
        Takes input from View, uses AI Model to predict category if it's an expense,
        and saves it to Database Model.
        """
        try:
            if t_type == "Expense" and not category:
                category = self.ai.predict_category(description)
            elif not category:
                category = "Income"
            
            self.db.add_transaction(user_id, t_type, date, description, float(amount), category)
            return category
        except Exception as e:
            raise Exception(f"Failed to add transaction: {str(e)}")

    def import_csv(self, filepath, user_id):
        """
        Reads a CSV, predicts categories, and saves to database.
        Assumes imported CSVs are Expenses.
        """
        imported_count = 0
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        date = row[0].strip()
                        description = row[1].strip()
                        try:
                            amount = float(row[2].strip())
                            # Predict and Save
                            category = self.ai.predict_category(description)
                            self.db.add_transaction(user_id, "Expense", date, description, amount, category)
                            imported_count += 1
                        except ValueError:
                            print(f"Skipping row with invalid amount: {row}")
            return imported_count
        except FileNotFoundError:
            raise Exception("The selected CSV file was not found.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during import: {str(e)}")

    def get_transactions(self, user_id):
        return self.db.get_user_transactions(user_id)
    
    def clear_all(self, user_id):
        self.db.clear_user_data(user_id)

    def export_data(self, filepath, user_id, format_type="csv"):
        transactions = self.get_transactions(user_id)
        if not transactions:
            raise Exception("No data to export.")
            
        if format_type.lower() == "csv":
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Description", "Amount", "Category", "Type"])
                for t in transactions:
                    writer.writerow(t)
        elif format_type.lower() == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Personal Finance Report", ln=True, align='C')
            
            # Simple table header
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(30, 10, "Date", 1)
            pdf.cell(60, 10, "Description", 1)
            pdf.cell(30, 10, "Amount", 1)
            pdf.cell(40, 10, "Category", 1)
            pdf.cell(30, 10, "Type", 1)
            pdf.ln()
            
            pdf.set_font("Arial", '', 10)
            for t in transactions:
                pdf.cell(30, 10, str(t[1])[:10], 1)
                pdf.cell(60, 10, str(t[2])[:30], 1)
                pdf.cell(30, 10, f"${t[3]:.2f}", 1)
                pdf.cell(40, 10, str(t[4])[:20], 1)
                pdf.cell(30, 10, str(t[5]), 1)
                pdf.ln()
                
            pdf.output(filepath)
        else:
            raise Exception("Unsupported export format.")
