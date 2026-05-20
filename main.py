import sys
import os

# Add the project root to the sys.path so we can import src modules easily
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.view.main_window import MainWindow

if __name__ == "__main__":
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Fatal Error: The application crashed. Details: {e}")
