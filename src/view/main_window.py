import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.controller.app_controller import AppController

# Setting up the professional dark theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Personal Finance & Expense Categorizer")
        self.geometry("800x600")
        
        self.controller = AppController()

        self._build_ui()
        self._refresh_table()

    def _build_ui(self):
        # Top Frame for controls
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=20, padx=20, fill="x")

        self.lbl_title = ctk.CTkLabel(self.top_frame, text="Smart Expense Tracker", font=("Helvetica", 24, "bold"))
        self.lbl_title.pack(pady=10)

        # Import CSV Button
        self.btn_import = ctk.CTkButton(self.top_frame, text="Import CSV Bank Statement", command=self.import_csv)
        self.btn_import.pack(side="left", padx=20, pady=10)

        # Clear DB Button
        self.btn_clear = ctk.CTkButton(self.top_frame, text="Clear Data", fg_color="red", hover_color="darkred", command=self.clear_data)
        self.btn_clear.pack(side="right", padx=20, pady=10)

        # Bottom Frame for data viewing
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.textbox = ctk.CTkTextbox(self.bottom_frame, font=("Courier", 14))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def import_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Bank Statement",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if filepath:
            try:
                count = self.controller.import_csv(filepath)
                messagebox.showinfo("Success", f"Successfully imported and AI-categorized {count} transactions.")
                self._refresh_table()
            except Exception as e:
                # Localized Exception Handling
                messagebox.showerror("Import Error", str(e))

    def clear_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all transactions?"):
            self.controller.clear_all()
            self._refresh_table()

    def _refresh_table(self):
        self.textbox.delete("1.0", ctk.END)
        transactions = self.controller.get_transactions()
        
        header = f"{'ID':<5} | {'Date':<12} | {'Description':<30} | {'Amount':<10} | {'AI Category'}\n"
        self.textbox.insert(ctk.END, header)
        self.textbox.insert(ctk.END, "-"*85 + "\n")
        
        for txn in transactions:
            row = f"{txn[0]:<5} | {txn[1]:<12} | {txn[2][:28]:<30} | ${txn[3]:<9.2f} | {txn[4]}\n"
            self.textbox.insert(ctk.END, row)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
