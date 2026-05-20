import pytest
from src.model.ai_model import ExpenseCategorizerAI

@pytest.fixture
def ai_model():
    model = ExpenseCategorizerAI()
    model.train()
    return model

def test_ai_categorizes_transportation(ai_model):
    prediction = ai_model.predict_category("Uber ride to airport")
    assert prediction == "Transportation"

def test_ai_categorizes_food(ai_model):
    prediction = ai_model.predict_category("Lunch at McDonalds")
    assert prediction == "Food & Dining"

def test_ai_categorizes_entertainment(ai_model):
    prediction = ai_model.predict_category("Netflix monthly fee")
    assert prediction == "Entertainment"

def test_ai_categorizes_utilities(ai_model):
    prediction = ai_model.predict_category("Electric Bill Payment")
    assert prediction == "Utilities"
