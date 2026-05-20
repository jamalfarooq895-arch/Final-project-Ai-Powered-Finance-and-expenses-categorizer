# Final Project Report: AI-Powered Personal Finance & Expense Categorizer

## 1. Process Model Selection & Justification
**Model Selected: Agile (Scrum/Iterative)**
I chose the Agile process model because integrating an Artificial Intelligence model (Scikit-Learn NLP) into a desktop application is an iterative process. It requires continuous tuning of the prediction algorithms, coupled with iterative UI enhancements using CustomTkinter. The project was broken down into manageable phases (Legacy setup -> MVC Refactoring -> AI Integration -> Testing).

## 2. Software Process Improvement (SPI)
During the semester, an initial bottleneck was discovered: manually testing the AI's categorization logic through the GUI was time-consuming and error-prone. To improve our software development process, we integrated **Automated Unit Testing** using `pytest`. This SPI drastically reduced regression bugs when the AI training dataset was modified.

## 3. Version Control
Git was used throughout the semester for version control. Commits were made logically, separating UI updates from Database schema changes and AI logic improvements.

## 4. Lehman’s Law Justification
This project demonstrates Lehman's **Law of Continuing Change** and **Law of Increasing Complexity**. 
- Initially, the project was a single procedural script (`legacy/old_script.py`) that used messy IF/ELSE statements.
- As "user demands" (simulated) required better accuracy, the software evolved. The hardcoded IF statements could not scale to hundreds of transaction types, thus forcing the system to evolve into a Machine Learning approach using TF-IDF and Naive Bayes, validating Lehman's Law that software must be continually adapted or become progressively less satisfactory.

## 5. Software Deployment
The system is built as a local Desktop Application. Deployment is managed by packaging the Python source code, `venv`, and SQLite database into an executable using PyInstaller. Users can simply run the `.exe` without needing Python installed locally.

## 6. Refactoring Legacy Code
The source code underwent a massive refactoring phase. The original procedural code (`legacy/old_script.py`) was refactored into the **Model-View-Controller (MVC)** design pattern. This separated the Database logic (`model/database.py`), the UI (`view/main_window.py`), and the business logic (`controller/app_controller.py`), removing legacy technical debt.

## 7. Unit Testing
Unit tests were written using `pytest`. They focus on verifying the AI Model's categorization accuracy (`tests/test_ai_model.py`) and ensuring the SQLite database maintains ACID compliance during insertions and deletions (`tests/test_database.py`).

## 8. Automated Testing
By writing `pytest` fixtures, the testing process is completely automated. Running `pytest tests/` automatically sets up a temporary mock database, runs the AI tests, asserts correct categorical predictions, and tears down the database without human intervention.

## 9. Exception Handling
Exception handling was applied comprehensively:
- **Global Try/Catch**: Wrap the entire application startup in `main.py` to prevent silent crashes.
- **Localized Exception Handling**: In `app_controller.py`, `try-except` blocks handle `ValueError` if a user imports a CSV with malformed amount strings, and `sqlite3.Error` blocks ensure database locks don't crash the UI.

## 10. Peer Reviews
(Simulated for Individual Project)
A peer review was conducted via a GitHub Pull Request before merging the `AI-Integration` branch into the `main` branch. The reviewer suggested moving the `TfidfVectorizer` pipeline inside the class `__init__` rather than initializing it globally, which improved memory management.

## 11. Team Roles & Contribution
Since this was an individual project, I utilized the "Multiple Hats" approach:
- **Systems Analyst**: Gathered requirements and designed the MVC architecture.
- **AI & Backend Developer**: Implemented the SQLite database and Scikit-Learn NLP model.
- **Frontend Developer**: Created the dark-mode responsive UI using CustomTkinter.
- **QA Tester**: Wrote and executed all Pytest scripts.
