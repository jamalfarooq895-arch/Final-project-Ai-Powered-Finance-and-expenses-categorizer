import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime
from src.controller.app_controller import AppController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self, user_id, on_logout):
        super().__init__()

        self.user_id = user_id
        self.on_logout = on_logout
        self.title("AI Personal Finance Dashboard")
        self.geometry("1100x700")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.controller = AppController()

        self._build_sidebar()
        self._build_main_area()
        self._refresh_dashboard()

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Finance AI", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_add_income = ctk.CTkButton(self.sidebar_frame, text="Add Salary/Income", command=self.add_income)
        self.btn_add_income.grid(row=1, column=0, padx=20, pady=10)

        self.btn_import = ctk.CTkButton(self.sidebar_frame, text="Import Expenses (CSV)", command=self.import_csv)
        self.btn_import.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_export_csv = ctk.CTkButton(self.sidebar_frame, text="Download CSV", command=lambda: self.export_data("csv"))
        self.btn_export_csv.grid(row=3, column=0, padx=20, pady=10)

        self.btn_export_pdf = ctk.CTkButton(self.sidebar_frame, text="Download PDF", command=lambda: self.export_data("pdf"))
        self.btn_export_pdf.grid(row=4, column=0, padx=20, pady=10)

        self.btn_clear = ctk.CTkButton(self.sidebar_frame, text="Clear Data", fg_color="#C21807", hover_color="#A51505", command=self.clear_data)
        self.btn_clear.grid(row=5, column=0, padx=20, pady=10)
        
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Logout", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.logout)
        self.btn_logout.grid(row=6, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Status: AI Active", text_color="green", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=9, column=0, padx=20, pady=20, sticky="s")

    def _build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Stat Cards
        self.card_salary = self._create_stat_card(self.main_frame, 0, "Total Salary/Income", "$0.00")
        self.card_spending = self._create_stat_card(self.main_frame, 1, "Total Spending", "$0.00")
        self.card_savings = self._create_stat_card(self.main_frame, 2, "Total Savings", "$0.00")

        # Chart Frame
        self.chart_frame = ctk.CTkFrame(self.main_frame)
        self.chart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(20, 20))
        
        # Transaction Grid
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Recent Transactions")
        self.scroll_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

    def _create_stat_card(self, parent, col, title, initial_value):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=col, sticky="nsew", padx=10)
        lbl_title = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        lbl_title.pack(pady=(15, 0))
        lbl_val = ctk.CTkLabel(frame, text=initial_value, font=ctk.CTkFont(size=24, weight="bold"))
        lbl_val.pack(pady=(0, 15))
        return lbl_val

    def add_income(self):
        amount = simpledialog.askfloat("Input", "Enter Salary/Income Amount ($):", parent=self)
        if amount:
            date = datetime.now().strftime("%Y-%m-%d")
            desc = "Salary/Income"
            try:
                self.controller.add_single_transaction(self.user_id, "Income", date, desc, amount)
                self._refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def import_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Bank Statement (Expenses)",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if filepath:
            try:
                count = self.controller.import_csv(filepath, self.user_id)
                messagebox.showinfo("Success", f"Successfully imported and AI-categorized {count} expense transactions.")
                self._refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Import Error", str(e))

    def export_data(self, format_type):
        ext = f".{format_type}"
        filepath = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=((f"{format_type.upper()} files", f"*{ext}"), ("All files", "*.*"))
        )
        if filepath:
            try:
                self.controller.export_data(filepath, self.user_id, format_type)
                messagebox.showinfo("Success", f"Report downloaded successfully as {format_type.upper()}.")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def clear_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all your transactions?"):
            self.controller.clear_all(self.user_id)
            self._refresh_dashboard()

    def logout(self):
        self.on_logout()

    def _refresh_dashboard(self):
        transactions = self.controller.get_transactions(self.user_id)
        
        total_salary = 0.0
        total_spending = 0.0
        category_totals = {}
        
        for t in transactions:
            t_type = t[5]
            amount = t[3]
            cat = t[4]
            
            if t_type == "Income":
                total_salary += amount
            elif t_type == "Expense":
                total_spending += amount
                category_totals[cat] = category_totals.get(cat, 0) + amount
                
        total_savings = total_salary - total_spending

        self.card_salary.configure(text=f"${total_salary:.2f}")
        self.card_spending.configure(text=f"${total_spending:.2f}")
        self.card_savings.configure(text=f"${total_savings:.2f}")

        # Highlight negative savings in red
        if total_savings < 0:
            self.card_savings.configure(text_color="#C21807")
        else:
            self.card_savings.configure(text_color=("gray10", "#DCE4EE"))

        self._draw_chart(category_totals)
        self._populate_grid(transactions)

    def _draw_chart(self, category_totals):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not category_totals:
            lbl = ctk.CTkLabel(self.chart_frame, text="No expense data to display chart.")
            lbl.pack(expand=True)
            return

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        
        fig, ax = plt.subplots(figsize=(6, 3), facecolor='#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90,
            textprops=dict(color="white"),
            wedgeprops=dict(width=0.4, edgecolor='#2b2b2b')
        )
        ax.axis('equal') 
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _populate_grid(self, transactions):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not transactions:
            return

        headers = ["Date", "Description", "Amount", "Category", "Type"]
        for col, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.scroll_frame, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=col, sticky="w", padx=15, pady=5)
        
        for i, txn in enumerate(transactions, start=1):
            ctk.CTkLabel(self.scroll_frame, text=txn[1]).grid(row=i, column=0, sticky="w", padx=15, pady=2)
            ctk.CTkLabel(self.scroll_frame, text=txn[2][:30]).grid(row=i, column=1, sticky="w", padx=15, pady=2)
            ctk.CTkLabel(self.scroll_frame, text=f"${txn[3]:.2f}").grid(row=i, column=2, sticky="w", padx=15, pady=2)
            ctk.CTkLabel(self.scroll_frame, text=txn[4], text_color="#1f6aa5").grid(row=i, column=3, sticky="w", padx=15, pady=2)
            
            type_color = "green" if txn[5] == "Income" else "red"
            ctk.CTkLabel(self.scroll_frame, text=txn[5], text_color=type_color).grid(row=i, column=4, sticky="w", padx=15, pady=2)

