import customtkinter as ctk

class StorekeeperDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Панель Кладовщика")
        self.geometry("500x400")

        ctk.CTkLabel(self, text="Добро пожаловать, Кладовщик!", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Приёмка товаров", command=self.receive_goods).pack(pady=10)
        ctk.CTkButton(self, text="Учёт остатков", command=self.stock_control).pack(pady=10)
        ctk.CTkButton(self, text="Отгрузка продукции", command=self.ship_goods).pack(pady=10)
        ctk.CTkButton(self, text="Выход", command=self.quit).pack(pady=20)

    def receive_goods(self):

    def stock_control(self):

    def ship_goods(self):

if __name__ == "__main__":
    app = StorekeeperDashboard()
    app.mainloop()
