import customtkinter as ctk
import tkinter as tk
import pymysql
import random
import re
from tkinter import W, CENTER, E

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"


class StorekeeperDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Окно кладовщика")
        self.geometry("100x100")
        self.center_window(700, 350)
        self.resizable(False, False)

        button_width = 200
        button_height = 120
        padding = 20

        self.view_stock_btn = self.create_tile_button("Просмотр склада", self.view_stock)
        self.view_stock_btn.place(relx=0.05, rely=0.25, anchor=W)

        self.receive_goods_btn = self.create_tile_button("Приём поставок", self.receive_goods)
        self.receive_goods_btn.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.write_off_btn = self.create_tile_button("Списание брака", self.write_off_goods)
        self.write_off_btn.place(relx=0.95, rely=0.25, anchor=E)

        self.report_btn = self.create_tile_button("Отчет по складу", self.stock_report)
        self.report_btn.place(relx=0.05, rely=0.65, anchor=W)

        self.check_barcode_btn = self.create_tile_button("Проверить штрих-код", self.check_barcode)
        self.check_barcode_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.logout_btn = self.create_tile_button("Выход", self.logout)
        self.logout_btn.place(relx=0.95, rely=0.65, anchor=E)

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

    def check_barcode(self):
        def submit():
            barcode = entry_barcode.get()
            result = random.choice(["Продукция легальна!", "Ошибка проверки в ЕГАИС!"])
            result_label.configure(text=result, text_color="green" if "✅" in result else "red")

        barcode_window = ctk.CTkToplevel(self)
        barcode_window.title("Проверка в ЕГАИС")
        barcode_window.geometry("300x200")
        barcode_window.transient(self)
        barcode_window.grab_set()
        barcode_window.focus_set()

        ctk.CTkLabel(barcode_window, text="Введите или сканируйте штрих-код:").pack()
        entry_barcode = ctk.CTkEntry(barcode_window)
        entry_barcode.pack()

        result_label = ctk.CTkLabel(barcode_window, text="")
        result_label.pack()

        ctk.CTkButton(barcode_window, text="Проверить", command=submit).pack(pady=10)

    def view_stock(self):
        stock_window = ctk.CTkToplevel(self)
        stock_window.title("Склад")
        stock_window.geometry("815x500")

        stock_window.transient(self)
        stock_window.grab_set()
        stock_window.focus_set()

        header_frame = ctk.CTkFrame(stock_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(header_frame, text="ID", width=50, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Наименование", width=200, anchor="w").grid(row=0, column=1, padx=10, pady=5,
                                                                                    sticky="w")
        ctk.CTkLabel(header_frame, text="Объем (L)", width=100, anchor="w").grid(row=0, column=2, padx=10, pady=5,
                                                                                 sticky="w")
        ctk.CTkLabel(header_frame, text="Крепость (%)", width=100, anchor="w").grid(row=0, column=3, padx=10, pady=5,
                                                                                    sticky="w")
        ctk.CTkLabel(header_frame, text="Количество (шт)", width=100, anchor="w").grid(row=0, column=4, padx=10, pady=5,
                                                                                       sticky="w")
        ctk.CTkLabel(header_frame, text="Цена", width=100, anchor="w").grid(row=0, column=5, padx=10, pady=5, sticky="w")

        canvas = ctk.CTkCanvas(stock_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(stock_window, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.update_idletasks()

        with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, volume, strength, quantity, price FROM stock")
            items = cursor.fetchall()

        for i, item in enumerate(items):
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(row_frame, text=str(item[0]), width=50, anchor="w").grid(row=0, column=0, padx=10, pady=2,
                                                                                  sticky="w")
            ctk.CTkLabel(row_frame, text=item[1], width=200, anchor="w").grid(row=0, column=1, padx=10, pady=2,
                                                                              sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[2]), width=100, anchor="w").grid(row=0, column=2, padx=10, pady=2,
                                                                                   sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[3]), width=100, anchor="w").grid(row=0, column=3, padx=10, pady=2,
                                                                                   sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[4]), width=100, anchor="w").grid(row=0, column=4, padx=10, pady=2,
                                                                                   sticky="w")
            ctk.CTkLabel(row_frame, text=f"{item[5]:.2f} руб.", width=100, anchor="w").grid(row=0, column=5, padx=10,
                                                                                            pady=2, sticky="w")

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def receive_goods(self):
        receive_window = ctk.CTkToplevel(self)
        receive_window.title("Приём поставок")
        receive_window.geometry("500x400")
        receive_window.transient(self)
        receive_window.grab_set()
        receive_window.focus_set()

        with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT DISTINCT t.purchase_id
            FROM transactions t
            WHERE t.status = 'pending' AND t.purchase_id IS NOT NULL
            """)
            pending_deliveries = cursor.fetchall()

        if not pending_deliveries:
            ctk.CTkLabel(receive_window, text="Нет ожидающих поставок").pack()
            return

        deliveries_dropdown = ctk.CTkOptionMenu(
            receive_window,
            values=[f"Поставка #{d[0]}" for d in pending_deliveries],
            command=lambda value: self.show_items(value, receive_window)
        )
        deliveries_dropdown.pack(pady=10)

    def show_items(self, selected_delivery, receive_window):
        delivery_id_match = re.search(r"#(\d+)", selected_delivery)

        if delivery_id_match:
            selected_delivery_id = int(delivery_id_match.group(1))
        else:
            return

        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT product_id, quantity FROM transactions WHERE purchase_id=%s AND status='pending'",
                (selected_delivery_id,))
            products = cursor.fetchall()

            if not products:
                ctk.CTkLabel(receive_window, text="Нет товаров для этой поставки").pack()
                return

            for widget in receive_window.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.destroy()

            self.deliveries_checkbox_list = []
            for product_id, quantity in products:
                cursor.execute("SELECT name, volume, strength FROM products WHERE id=%s", (product_id,))
                product_name, volume, strength = cursor.fetchone()

                checkbox = ctk.CTkCheckBox(receive_window,
                                           text=f"{product_name} - {quantity} шт. ({volume} L, {strength}%)",
                                           onvalue=product_id,
                                           offvalue=0)
                self.deliveries_checkbox_list.append(
                    (checkbox, quantity))
                checkbox.pack(anchor="w")

            ctk.CTkButton(receive_window, text="Завершить приём поставки",
                          command=lambda: self.accept_delivery(selected_delivery_id, receive_window)).pack(pady=10)

        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")

        finally:
            if conn:
                conn.close()

    def accept_delivery(self, selected_purchase_id, receive_window):
        selected_items = [(checkbox.get(), quantity) for checkbox, quantity in self.deliveries_checkbox_list if
                          checkbox.get() != 0]
        if not selected_items:
            ctk.CTkLabel(receive_window, text="Не выбраны товары для приёма").pack()
            return

        try:
            with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
                cursor = conn.cursor()

                for product_id, quantity in selected_items:
                    cursor.execute("SELECT name, volume, strength, price FROM products WHERE id=%s", (product_id,))
                    name, volume, strength, unit_price = cursor.fetchone()

                    total_price = unit_price * quantity

                    cursor.execute(
                        """INSERT INTO stock (product_id, name, volume, strength, quantity, price) 
                           VALUES (%s, %s, %s, %s, %s, %s) 
                           ON DUPLICATE KEY UPDATE 
                           quantity = quantity + VALUES(quantity), 
                           price = VALUES(price)""",
                        (product_id, name, volume, strength, quantity, total_price)
                    )

                    cursor.execute(
                        "UPDATE transactions SET status='received' WHERE purchase_id=%s AND product_id=%s",
                        (selected_purchase_id, product_id))

                conn.commit()
                print("Поставка принята!")
                receive_window.destroy()

        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")

    def write_off_goods(self):
        write_off_window = ctk.CTkToplevel(self)
        write_off_window.title("Списание товара")
        write_off_window.geometry("835x500")

        write_off_window.transient(self)
        write_off_window.grab_set()
        write_off_window.focus_set()

        header_frame = ctk.CTkFrame(write_off_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(header_frame, text="ID", width=50, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(header_frame, text="Наименование", width=200, anchor="w").grid(row=0, column=1, padx=10, pady=5,
                                                                                    sticky="w")
        ctk.CTkLabel(header_frame, text="Объем (L)", width=100, anchor="w").grid(row=0, column=2, padx=10, pady=5,
                                                                                 sticky="w")
        ctk.CTkLabel(header_frame, text="Крепость (%)", width=100, anchor="w").grid(row=0, column=3, padx=10, pady=5,
                                                                                    sticky="w")
        ctk.CTkLabel(header_frame, text="Количество (шт)", width=100, anchor="w").grid(row=0, column=4, padx=10, pady=5,
                                                                                       sticky="w")

        canvas = ctk.CTkCanvas(write_off_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(write_off_window, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.update_idletasks()

        with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, volume, strength, quantity FROM stock")
            items = cursor.fetchall()

        item_buttons = []
        for i, item in enumerate(items):
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(row_frame, text=str(item[0]), width=50, anchor="w").grid(row=0, column=0, padx=10, pady=2,
                                                                                  sticky="w")
            ctk.CTkLabel(row_frame, text=item[1], width=200, anchor="w").grid(row=0, column=1, padx=10, pady=2,
                                                                              sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[2]), width=100, anchor="w").grid(row=0, column=2, padx=10, pady=2,
                                                                                   sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[3]), width=100, anchor="w").grid(row=0, column=3, padx=10, pady=2,
                                                                                   sticky="w")
            ctk.CTkLabel(row_frame, text=str(item[4]), width=100, anchor="w").grid(row=0, column=4, padx=10, pady=2,
                                                                                   sticky="w")

            item_button = ctk.CTkButton(row_frame, text="Выбрать",
                                        command=lambda item=item: self.select_item_for_write_off(write_off_window,
                                                                                                 item))
            item_button.grid(row=0, column=5, padx=10, pady=2)

            item_buttons.append(item_button)

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def select_item_for_write_off(self, write_off_window, item):
        write_off_window.destroy()

        write_off_detail_window = ctk.CTkToplevel(self)
        write_off_detail_window.title("Детали списания товара")
        write_off_detail_window.geometry("500x400")

        write_off_detail_window.transient(self)
        write_off_detail_window.grab_set()
        write_off_detail_window.focus_set()

        ctk.CTkLabel(write_off_detail_window, text=f"Вы выбрали товар: {item[1]}").pack(padx=10, pady=5)
        ctk.CTkLabel(write_off_detail_window, text=f"Количество на складе: {item[4]} шт.").pack(padx=10, pady=5)

        quantity_label = ctk.CTkLabel(write_off_detail_window, text="Введите количество для списания:")
        quantity_label.pack(padx=10, pady=5)

        quantity_entry = ctk.CTkEntry(write_off_detail_window)
        quantity_entry.pack(padx=10, pady=5)

        reason_label = ctk.CTkLabel(write_off_detail_window, text="Выберите причину списания:")
        reason_label.pack(padx=10, pady=5)

        reasons = [
            "Повреждение упаковки",
            "Нарушение условий хранения",
            "Просроченный срок годности",
            "Несоответствие маркировки",
            "Мошенничество или подделка",
            "Неудовлетворительное качество продукта",
        ]

        reason_var = tk.StringVar()
        reason_menu = ctk.CTkOptionMenu(write_off_detail_window, variable=reason_var, values=reasons)
        reason_menu.pack(padx=10, pady=5)

        confirm_button = ctk.CTkButton(write_off_detail_window, text="Подтвердить списание",
                                       command=lambda: self.confirm_write_off(item, quantity_entry, reason_var,
                                                                              write_off_detail_window))
        confirm_button.pack(padx=10, pady=20)

    def confirm_write_off(self, item, quantity_entry, reason_var, write_off_detail_window):
        try:
            quantity = int(quantity_entry.get())
        except ValueError:
            ctk.CTkLabel(write_off_detail_window, text="Пожалуйста, введите корректное количество").pack(padx=10,
                                                                                                         pady=5)
            return

        reason = reason_var.get()

        if quantity <= 0:
            ctk.CTkLabel(write_off_detail_window, text="Количество должно быть больше 0").pack(padx=10, pady=5)
            return

        try:
            with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT quantity FROM stock WHERE id = %s", (item[0],))
                current_quantity = cursor.fetchone()

                if current_quantity is None:
                    ctk.CTkLabel(write_off_detail_window, text="Товар не найден в базе").pack(padx=10, pady=5)
                    return

                if current_quantity[0] < quantity:
                    ctk.CTkLabel(write_off_detail_window, text="Недостаточно товара для списания").pack(padx=10, pady=5)
                    return

                query = """
                INSERT INTO write_offs (stock_id, quantity, reason)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (item[0], quantity, reason))
                conn.commit()

                update_query = """
                UPDATE stock
                SET quantity = quantity - %s
                WHERE id = %s
                """
                cursor.execute(update_query, (quantity, item[0]))
                conn.commit()

            write_off_detail_window.destroy()

        except Exception as e:
            ctk.CTkLabel(write_off_detail_window, text=f"Ошибка: {str(e)}").pack(padx=10, pady=5)

    def stock_report(self):

        pass


if __name__ == "__main__":
    app = StorekeeperDashboard()
    app.mainloop()
