import customtkinter as ctk
import pymysql
import admin_panel


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Авторизация")
        self.geometry("600x400")
        self.center_window(600, 400)

        self.validate_50 = self.register(self.limit_50_chars)

        self.label_user = ctk.CTkLabel(self, text="Логин:")
        self.label_user.pack(pady=5)
        self.entry_user = ctk.CTkEntry(self, validate="key", validatecommand=(self.validate_50, "%P"))
        self.entry_user.pack(pady=5)

        self.label_pass = ctk.CTkLabel(self, text="Пароль:")
        self.label_pass.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self, show="*", validate="key", validatecommand=(self.validate_50, "%P"))
        self.entry_pass.pack(pady=5)

        self.button_login = self.create_tile_button("Войти", self.login)
        self.button_login.pack(pady=25)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    def create_tile_button(self, text, command):
        button = ctk.CTkButton(self, text=text, command=command, width=150, height=34, corner_radius=15,
                               fg_color="#3b8ed0", hover_color="#2971a4", font=('', 17))
        button.bind("<Enter>", lambda event, btn=button: btn.configure(fg_color="#2971a4"))
        button.bind("<Leave>", lambda event, btn=button: btn.configure(fg_color="#3b8ed0"))
        return button

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.withdraw()
            self.open_panel(role)
        else:
            self.error_label.configure(text="Неверный логин или пароль")

    def open_panel(self, role):
        username = self.entry_user.get()

        if role == "Администратор":
            admin_panel.AdminDashboard().mainloop()
        elif role == "Кладовщик":
            import storekeeper_panel
            storekeeper_panel.StorekeeperDashboard(username).mainloop()
        elif role == "Бухгалтер":
            import accountant_panel
            accountant_panel.AccountantDashboard(username).mainloop()

    def limit_50_chars(self, new_value):
        return len(new_value) <= 50


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
