import sys
import os

# Add the project root to the sys.path so we can import src modules easily
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.view.main_window import MainWindow
from src.view.login_window import LoginWindow

def start_app():
    def launch_main(user_id):
        # We define a function to start the login window when the user logs out
        def on_logout():
            main_app.destroy()
            start_app()

        main_app = MainWindow(user_id, on_logout)
        main_app.mainloop()

    login_app = LoginWindow(on_login_success=launch_main)
    login_app.mainloop()

if __name__ == "__main__":
    try:
        start_app()
    except Exception as e:
        print(f"Fatal Error: The application crashed. Details: {e}")

