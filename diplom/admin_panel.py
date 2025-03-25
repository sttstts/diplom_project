import customtkinter as ctk
import pymysql
from tkinter import messagebox

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Панель Администратора")
        self.geometry("600x400")
        self.center_window(600, 400)

        ctk.CTkLabel(self, text="Управление пользователями", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self, text="Просмотр пользователей", command=self.view_users).pack(pady=5)
        ctk.CTkButton(self, text="Добавить пользователя", command=self.add_user_window).pack(pady=5)
        ctk.CTkButton(self, text="Удалить пользователя", command=self.delete_user_window).pack(pady=5)
        ctk.CTkButton(self, text="Выход", command=self.logout).pack(pady=10)

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def logout(self):
        self.destroy()
        from login import LoginApp
        login_window = LoginApp()
        login_window.mainloop()

    def db_connect(self):
        return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

    def view_users(self):
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        user_list = "\n".join([f"{u[0]}. {u[1]} - {u[2]}" for u in users])
        messagebox.showinfo("Список пользователей", user_list if user_list else "Пользователей нет.")

    def add_user_window(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Добавить пользователя")
        add_window.geometry("300x250")

        ctk.CTkLabel(add_window, text="Логин:").pack()
        entry_username = ctk.CTkEntry(add_window)
        entry_username.pack()

        ctk.CTkLabel(add_window, text="Пароль:").pack()
        entry_password = ctk.CTkEntry(add_window, show="*")
        entry_password.pack()

        ctk.CTkLabel(add_window, text="Роль:").pack()
        role_var = ctk.StringVar(value="Кладовщик")
        role_menu = ctk.CTkOptionMenu(add_window, variable=role_var, values=["Кладовщик", "Бухгалтер"])
        role_menu.pack()

        add_window.transient(self)
        add_window.grab_set()
        add_window.focus_set()

        def add_user():
            username = entry_username.get()
            password = entry_password.get()
            role = role_var.get()
            if username and password:
                conn = self.db_connect()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                                   (username, password, role))
                    conn.commit()
                    messagebox.showinfo("Успех", "Пользователь добавлен.")
                    add_window.destroy()
                except pymysql.MySQLError:
                    messagebox.showerror("Ошибка", "Ошибка добавления пользователя.")
                finally:
                    conn.close()
            else:
                messagebox.showwarning("Внимание", "Все поля должны быть заполнены.")

        ctk.CTkButton(add_window, text="Добавить", command=add_user).pack(pady=10)

    def delete_user_window(self):
        del_window = ctk.CTkToplevel(self)
        del_window.title("Удалить пользователя")
        del_window.geometry("350x380")

        del_window.transient(self)
        del_window.grab_set()
        del_window.focus_set()

        ctk.CTkLabel(del_window, text="Выберите пользователя для удаления:").pack(pady=5)

        frame = ctk.CTkFrame(del_window)
        frame.pack(pady=5, fill="both", expand=True)

        user_listbox = ctk.CTkScrollableFrame(frame, width=300, height=150)
        user_listbox.pack()

        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE role != 'Администратор'")
        users = cursor.fetchall()
        conn.close()

        user_dict = {}
        for user in users:
            user_id, username, role = user
            user_dict[f"{username} ({role})"] = user_id
            ctk.CTkLabel(user_listbox, text=f"{username} ({role})").pack(anchor="w", padx=5, pady=2)

        selected_user = ctk.StringVar(value="")

        def confirm_delete():
            username_role = selected_user.get()
            if username_role and username_role in user_dict:
                user_id = user_dict[username_role]
                conn = self.db_connect()
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
                    conn.commit()
                    messagebox.showinfo("Успех", "Пользователь удалён.")
                    del_window.destroy()
                except pymysql.MySQLError:
                    messagebox.showerror("Ошибка", "Ошибка удаления пользователя.")
                finally:
                    conn.close()
            else:
                messagebox.showwarning("Внимание", "Выберите пользователя.")

        user_dropdown = ctk.CTkOptionMenu(del_window, variable=selected_user, values=list(user_dict.keys()))
        user_dropdown.pack(pady=5)

        ctk.CTkButton(del_window, text="Удалить", command=confirm_delete).pack(pady=10)

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
