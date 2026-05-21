# AI-Powered Personal Finance & Expense Categorizer

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-AI%2FML-orange.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![pytest](https://img.shields.io/badge/Testing-pytest-yellow.svg)

## Overview
The **AI-Powered Personal Finance Dashboard** is a desktop application built in Python that automatically categorizes personal expenses using Artificial Intelligence. Built with a robust Model-View-Controller (MVC) architecture, the system leverages a Scikit-Learn Natural Language Processing (NLP) model to intelligently analyze transaction descriptions and assign them to the correct financial categories. 

This project evolved from a simple procedural script with hardcoded logic into a fully scalable, AI-driven, and unit-tested desktop software.

## Features
- **🤖 Smart AI Categorization:** Replaces hardcoded IF/ELSE logic with a Machine Learning pipeline (TF-IDF Vectorization & Naive Bayes classifier) to automatically categorize expenses based on the transaction description.
- **📊 Modern User Interface:** Features a sleek, responsive, and dark-mode friendly GUI built with `CustomTkinter`.
- **💾 Embedded Database:** Utilizes SQLite for robust, local data storage, ensuring ACID compliance for all transaction records.
- **🏗️ MVC Architecture:** Clean separation of concerns between Database Logic (Model), UI (View), and Business Logic (Controller).
- **🛡️ Rock-Solid Reliability:** Comprehensive global and localized exception handling prevents silent crashes during file imports or database locks.
- **🧪 Automated Unit Testing:** Extensive test coverage using `pytest` for testing AI model accuracy and database integrity.

## Technologies Used
- **Language:** Python
- **AI/ML:** Scikit-Learn (`TfidfVectorizer`, `MultinomialNB`), Pandas
- **Frontend GUI:** CustomTkinter, Tkinter
- **Backend & Database:** SQLite
- **Testing:** pytest

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jamalfarooq895-arch/Final-project-Ai-Powered-Finance-and-expenses-categorizer.git
   cd Final-project-Ai-Powered-Finance-and-expenses-categorizer
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## Running Tests
To run the automated test suite, ensure your virtual environment is active and run:
```bash
pytest tests/
```
The test suite utilizes mock databases to automatically verify the AI's categorization logic and database insertions without affecting your production data.

## Project Architecture (MVC)
- **Model (`src/model/`):** Contains `database.py` for SQLite operations and `ai_model.py` for the Scikit-Learn logic.
- **View (`src/view/`):** Contains `main_window.py` and `login_window.py` for rendering the CustomTkinter GUI.
- **Controller (`src/controller/`):** Contains `app_controller.py` to bridge user inputs with the model and AI processing.

## License
[MIT License](LICENSE)
