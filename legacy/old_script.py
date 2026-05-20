import csv

# LEGACY CODE: This represents the "before" state of the project.
# It uses a messy, hardcoded approach instead of AI or proper architecture.
# We keep this file to demonstrate "Refactoring Legacy Code" in our final report.

def categorize_expense(description):
    desc = description.lower()
    
    # Very bad approach: Hardcoded IF statements
    if "mcdonalds" in desc or "restaurant" in desc or "pizza" in desc:
        return "Food & Dining"
    elif "uber" in desc or "gas" in desc or "fuel" in desc:
        return "Transportation"
    elif "netflix" in desc or "spotify" in desc or "cinema" in desc:
        return "Entertainment"
    elif "electric" in desc or "water" in desc or "internet" in desc:
        return "Utilities"
    else:
        return "Other"

def process_csv(filepath):
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            print("Date, Description, Amount, Category")
            for row in reader:
                if len(row) >= 3:
                    date = row[0]
                    description = row[1]
                    amount = row[2]
                    category = categorize_expense(description)
                    print(f"{date}, {description}, {amount}, {category}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    print("Welcome to the Legacy Expense Categorizer!")
    print("This script is hard to maintain and does not use AI.")
    # process_csv('sample_bank_statement.csv')
