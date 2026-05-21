import pytest
import os
from src.model.database import DatabaseManager

# Use a test database so we don't overwrite production data
TEST_DB_PATH = "test_finance_app.db"

@pytest.fixture
def db():
    # Setup
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            pass
    database = DatabaseManager(TEST_DB_PATH)
    yield database
    # Teardown
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            pass

def test_add_transaction(db):
    user_id = db.register_user("testuser", "password123")
    db.add_transaction(user_id, "Expense", "2023-10-01", "Uber to work", 15.50, "Transportation")
    transactions = db.get_user_transactions(user_id)
    assert len(transactions) == 1
    assert transactions[0][1] == "2023-10-01"
    assert transactions[0][2] == "Uber to work"
    assert transactions[0][3] == 15.50
    assert transactions[0][4] == "Transportation"
    assert transactions[0][5] == "Expense"

def test_clear_database(db):
    user_id = db.register_user("testuser2", "password123")
    db.add_transaction(user_id, "Expense", "2023-10-01", "Test", 10.0, "Other")
    db.add_transaction(user_id, "Income", "2023-10-02", "Test 2", 20.0, "Salary")
    assert len(db.get_user_transactions(user_id)) == 2
    
    db.clear_user_data(user_id)
    assert len(db.get_user_transactions(user_id)) == 0
