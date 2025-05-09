import customtkinter as ctk
import pymysql
from tkinter import messagebox
from logger import log_action
from tkinter import ttk

from PIL._tkinter_finder import tk

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AdminDashboard(ctk.CTk):
    def __init__(self, username="admin"):
        super().__init__()
        self.username = username
        self.title("Панель Администратора")
        self.geometry("600x400")
        self.center_window(600, 400)

        ctk.CTkLabel(self, text="Управление пользователями", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self, text="Просмотр пользователей", command=self.view_users).pack(pady=5)
        ctk.CTkButton(self, text="Добавить пользователя", command=self.add_user_window).pack(pady=5)
        ctk.CTkButton(self, text="Удалить пользователя", command=self.delete_user_window).pack(pady=5)
        ctk.CTkButton(self, text="Журнал действий", command=self.view_log).pack(pady=5)
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
        users_window = ctk.CTkToplevel(self)
        users_window.title("Список пользователей")
        users_window.geometry("600x500")

        users_window.transient(self)
        users_window.grab_set()
        users_window.focus_set()

        header_frame = ctk.CTkFrame(users_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        columns = ["ID", "Логин", "Роль"]
        widths = [50, 250, 200]

        for i, col in enumerate(columns):
            ctk.CTkLabel(header_frame, text=col, width=widths[i], anchor="w").grid(
                row=0, column=i, padx=10, pady=5, sticky="w"
            )

        canvas = ctk.CTkCanvas(users_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(users_window, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.update_idletasks()

        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(fill="x", padx=10, pady=2)

            for j, value in enumerate(user):
                ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    width=widths[j],
                    anchor="w"
                ).grid(row=0, column=j, padx=10, pady=2, sticky="w")

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        users_window.bind_all("<MouseWheel>", on_mouse_wheel)

        log_action("admin", "Просмотрел список пользователей")

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

                    log_action("admin", f"Добавил пользователя {username} с ролью {role}")

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

                    log_action("admin", f"Удалил пользователя {username_role}")

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

    def view_log(self):
        log_window = ctk.CTkToplevel(self)
        log_window.title("Журнал действий")
        log_window.geometry("855x500")

        log_window.transient(self)
        log_window.grab_set()
        log_window.focus_set()

        header_frame = ctk.CTkFrame(log_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        columns = ["ID", "Пользователь", "Действие", "Время"]
        widths = [50, 150, 415, 150]

        for i, col in enumerate(columns):
            ctk.CTkLabel(header_frame, text=col, width=widths[i], anchor="w").grid(row=0, column=i, padx=10, pady=5,
                                                                                   sticky="w")

        canvas = ctk.CTkCanvas(log_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(log_window, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.update_idletasks()

        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, action, timestamp FROM activity_log ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        conn.close()

        for i, log in enumerate(logs):
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(fill="x", padx=10, pady=2)

            id_, username, action, timestamp = log
            values = [id_, username, action, timestamp.strftime("%d.%m.%Y %H:%M:%S")]

            for j, value in enumerate(values):
                ctk.CTkLabel(row_frame, text=str(value), width=widths[j], anchor="w", justify="left",
                             wraplength=widths[j] - 10).grid(
                    row=0, column=j, padx=10, pady=2, sticky="w"
                )

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        log_window.bind_all("<MouseWheel>", on_mouse_wheel)

        log_action(self.username, "Просмотрел журнал действий")

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
