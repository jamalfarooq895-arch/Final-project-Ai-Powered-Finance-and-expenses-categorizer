import pytest
import os
from src.model.database import DatabaseManager

# Use a test database so we don't overwrite production data
TEST_DB_PATH = "test_finance_app.db"

@pytest.fixture
def db():
    # Setup
    database = DatabaseManager(TEST_DB_PATH)
    database.clear_database()
    yield database
    # Teardown
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_add_transaction(db):
    db.add_transaction("2023-10-01", "Uber to work", 15.50, "Transportation")
    transactions = db.get_all_transactions()
    assert len(transactions) == 1
    assert transactions[0][1] == "2023-10-01"
    assert transactions[0][2] == "Uber to work"
    assert transactions[0][3] == 15.50
    assert transactions[0][4] == "Transportation"

def test_clear_database(db):
    db.add_transaction("2023-10-01", "Test", 10.0, "Other")
    db.add_transaction("2023-10-02", "Test 2", 20.0, "Other")
    assert len(db.get_all_transactions()) == 2
    
    db.clear_database()
    assert len(db.get_all_transactions()) == 0
