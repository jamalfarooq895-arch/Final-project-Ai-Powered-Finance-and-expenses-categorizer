from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pandas as pd

class ExpenseCategorizerAI:
    def __init__(self):
        # We use a pipeline: TF-IDF vectorizes the text, and Naive Bayes classifies it.
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.is_trained = False

    def train(self):
        """
        Train the model using some dummy training data.
        In a real application, this would load a large CSV of past transactions.
        """
        data = {
            'description': [
                'Uber ride', 'Lyft trip', 'Shell gas station', 'Chevron',
                'McDonalds', 'Pizza Hut', 'Starbucks coffee', 'KFC',
                'Netflix subscription', 'Spotify Premium', 'AMC Cinema',
                'Electric Bill', 'Water Utilities', 'Comcast Internet',
                'Walmart Groceries', 'Target Store'
            ],
            'category': [
                'Transportation', 'Transportation', 'Transportation', 'Transportation',
                'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining',
                'Entertainment', 'Entertainment', 'Entertainment',
                'Utilities', 'Utilities', 'Utilities',
                'Shopping', 'Shopping'
            ]
        }
        
        df = pd.DataFrame(data)
        
        try:
            # Training the scikit-learn model
            self.model.fit(df['description'], df['category'])
            self.is_trained = True
        except Exception as e:
            raise Exception(f"Failed to train AI model: {str(e)}")

    def predict_category(self, description):
        """
        Predicts the category of a given transaction description.
        """
        if not self.is_trained:
            self.train()
            
        try:
            prediction = self.model.predict([description])
            return prediction[0]
        except Exception as e:
            # Global exception handling requirement
            return "Uncategorized"
