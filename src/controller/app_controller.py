import csv
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

    def add_single_transaction(self, date, description, amount):
        """
        Takes input from View, uses AI Model to predict category,
        and saves it to Database Model.
        """
        try:
            category = self.ai.predict_category(description)
            self.db.add_transaction(date, description, float(amount), category)
            return category
        except Exception as e:
            raise Exception(f"Failed to add transaction: {str(e)}")

    def import_csv(self, filepath):
        """
        Reads a CSV, predicts categories, and saves to database.
        Includes extensive exception handling as per SCD requirements.
        """
        imported_count = 0
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                # Assuming format: Date, Description, Amount
                for row in reader:
                    if len(row) >= 3:
                        date = row[0].strip()
                        description = row[1].strip()
                        try:
                            amount = float(row[2].strip())
                            # Predict and Save
                            category = self.ai.predict_category(description)
                            self.db.add_transaction(date, description, amount, category)
                            imported_count += 1
                        except ValueError:
                            print(f"Skipping row with invalid amount: {row}")
            return imported_count
        except FileNotFoundError:
            raise Exception("The selected CSV file was not found.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during import: {str(e)}")

    def get_transactions(self):
        return self.db.get_all_transactions()
    
    def clear_all(self):
        self.db.clear_database()
