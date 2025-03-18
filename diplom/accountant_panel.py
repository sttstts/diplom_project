import customtkinter as ctk

class AccountantDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Панель Бухгалтера")
        self.geometry("500x400")

        ctk.CTkLabel(self, text="Добро пожаловать, Бухгалтер!", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Учёт продаж", command=self.sales_record).pack(pady=10)
        ctk.CTkButton(self, text="Формирование отчетов", command=self.generate_reports).pack(pady=10)
        ctk.CTkButton(self, text="Контроль платежей", command=self.payment_control).pack(pady=10)
        ctk.CTkButton(self, text="Выход", command=self.quit).pack(pady=20)

    def sales_record(self):

    def generate_reports(self):

    def payment_control(self):

if __name__ == "__main__":
    app = AccountantDashboard()
    app.mainloop()
