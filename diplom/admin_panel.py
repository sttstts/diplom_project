import customtkinter as ctk
import pymysql
from tkinter import messagebox
from logger import log_action
from tkinter import W, CENTER, E
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AdminDashboard(ctk.CTk):
    def __init__(self, username="admin"):
        super().__init__()
        self.username = username
        self.title("Панель Администратора")
        self.geometry("700x350")
        self.center_window(700, 350)
        self.resizable(False, False)

        self.validate_50 = self.register(self.limit_50_chars)

        self.add_user_btn = self.create_tile_button("Добавить пользователя", self.add_user_window)
        self.add_user_btn.place(relx=0.2, rely=0.25, anchor=W)

        self.delete_user_btn = self.create_tile_button("Удалить пользователя", self.delete_user_window)
        self.delete_user_btn.place(relx=0.65, rely=0.25, anchor=CENTER)

        self.view_users_btn = self.create_tile_button("Просмотр пользователей", self.view_users)
        self.view_users_btn.place(relx=0.05, rely=0.65, anchor=W)

        self.log_btn = self.create_tile_button("Журнал действий", self.view_log)
        self.log_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.exit_btn = self.create_tile_button("Выход", self.logout)
        self.exit_btn.place(relx=0.95, rely=0.65, anchor=E)

    def create_tile_button(self, text, command):
        button = ctk.CTkButton(self, text=text, command=command, width=200, height=120, corner_radius=15,
                               fg_color="#3b8ed0", hover_color="#2971a4", font=('', 15))
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
        entry_username = ctk.CTkEntry(add_window, validate="key", validatecommand=(self.validate_50, "%P"))
        entry_username.pack()

        ctk.CTkLabel(add_window, text="Пароль:").pack()
        entry_password = ctk.CTkEntry(add_window, show="*", validate="key", validatecommand=(self.validate_50, "%P"))
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
        log_window.geometry("950x600")

        log_window.transient(self)
        log_window.grab_set()
        log_window.focus_set()

        search_frame = ctk.CTkFrame(log_window)
        search_frame.pack(fill="x", padx=10, pady=(10, 5))

        username_entry = ctk.CTkEntry(search_frame, placeholder_text="Имя пользователя")
        username_entry.pack(side="left", padx=5)

        date_from_entry = ctk.CTkEntry(search_frame, placeholder_text="От (дд.мм.гггг)")
        date_from_entry.pack(side="left", padx=5)

        date_to_entry = ctk.CTkEntry(search_frame, placeholder_text="До (дд.мм.гггг)")
        date_to_entry.pack(side="left", padx=5)

        def fetch_logs():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            query = "SELECT id, username, action, timestamp FROM activity_log WHERE 1=1"
            params = []

            username = username_entry.get().strip()
            date_from = date_from_entry.get().strip()
            date_to = date_to_entry.get().strip()

            if username:
                query += " AND username LIKE %s"
                params.append(f"%{username}%")

            if date_from:
                try:
                    date_from_obj = datetime.strptime(date_from, "%d.%m.%Y")
                    query += " AND timestamp >= %s"
                    params.append(date_from_obj)
                except ValueError:
                    ctk.CTkLabel(scrollable_frame, text="Неверный формат даты 'От'", text_color="red").pack()
                    return

            if date_to:
                try:
                    date_to_obj = datetime.strptime(date_to, "%d.%m.%Y")
                    date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
                    query += " AND timestamp <= %s"
                    params.append(date_to_obj)
                except ValueError:
                    ctk.CTkLabel(scrollable_frame, text="Неверный формат даты 'До'", text_color="red").pack()
                    return

            query += " ORDER BY timestamp DESC"

            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
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

        search_button = ctk.CTkButton(search_frame, text="Поиск", command=fetch_logs)
        search_button.pack(side="left", padx=5)

        header_frame = ctk.CTkFrame(log_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        columns = ["ID", "Пользователь", "Действие", "Время"]
        widths = [50, 150, 415, 200]

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
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        log_window.bind_all("<MouseWheel>", on_mouse_wheel)

        fetch_logs()

        log_action(self.username, "Просмотрел журнал действий")

    def limit_50_chars(self, new_value):
        return len(new_value) <= 50

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
