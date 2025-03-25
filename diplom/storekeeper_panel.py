import customtkinter as ctk
import pymysql
import random
import re

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"


class StorekeeperDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Окно кладовщика")
        self.geometry("600x400")
        self.center_window(600, 400)

        self.view_stock_btn = ctk.CTkButton(self, text="Просмотр склада", command=self.view_stock)
        self.view_stock_btn.pack(pady=5)

        self.receive_goods_btn = ctk.CTkButton(self, text="Приём поставок", command=self.receive_goods)
        self.receive_goods_btn.pack(pady=5)

        self.write_off_btn = ctk.CTkButton(self, text="Списание брака", command=self.write_off_goods)
        self.write_off_btn.pack(pady=5)

        self.report_btn = ctk.CTkButton(self, text="Отчет по складу", command=self.stock_report)
        self.report_btn.pack(pady=5)

        self.check_barcode_btn = ctk.CTkButton(self, text="Проверить штрих-код (ЕГАИС)", command=self.check_barcode)
        self.check_barcode_btn.pack(pady=5)

        self.logout_btn = ctk.CTkButton(self, text="Выход", command=self.logout)
        self.logout_btn.pack(pady=10)

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
        stock_window.geometry("400x300")

        stock_window.transient(self)
        stock_window.grab_set()
        stock_window.focus_set()

        with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, volume, strength, quantity, price FROM stock")
            items = cursor.fetchall()

        for item in items:
            ctk.CTkLabel(stock_window, text=f"{item[0]}. {item[1]} - {item[4]} шт. ({item[2]} L, {item[3]}%)").pack()

    def receive_goods(self):
        receive_window = ctk.CTkToplevel(self)
        receive_window.title("Приём поставок")
        receive_window.geometry("500x400")
        receive_window.transient(self)
        receive_window.grab_set()
        receive_window.focus_set()

        # Подключение к базе данных
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

        # Список поставок для выбора
        deliveries_dropdown = ctk.CTkOptionMenu(
            receive_window,
            values=[f"Поставка #{d[0]}" for d in pending_deliveries],
            command=lambda value: self.show_items(value, receive_window)  # Передаем значение и окно
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

            # Запрашиваем все товары из выбранной поставки
            cursor.execute(
                "SELECT product_id, quantity FROM transactions WHERE purchase_id=%s AND status='pending'",
                (selected_delivery_id,))
            products = cursor.fetchall()

            if not products:
                ctk.CTkLabel(receive_window, text="Нет товаров для этой поставки").pack()
                return

            # Очистка предыдущих чекбоксов
            for widget in receive_window.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.destroy()

            self.deliveries_checkbox_list = []
            for product_id, quantity in products:
                # Получаем данные о продукте
                cursor.execute("SELECT name, volume, strength FROM products WHERE id=%s", (product_id,))
                product_name, volume, strength = cursor.fetchone()

                # Создаем чекбоксы для каждого товара
                checkbox = ctk.CTkCheckBox(receive_window,
                                           text=f"{product_name} - {quantity} шт. ({volume} L, {strength}%)",
                                           onvalue=product_id,
                                           offvalue=0)
                self.deliveries_checkbox_list.append(
                    (checkbox, quantity))  # Сохраняем количество вместе с чекбоксом
                checkbox.pack(anchor="w")

            # Кнопка для принятия товаров
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
                    # Получаем информацию о продукте
                    cursor.execute("SELECT name, volume, strength, price FROM products WHERE id=%s", (product_id,))
                    name, volume, strength, unit_price = cursor.fetchone()

                    # Рассчитываем общую цену
                    total_price = unit_price * quantity

                    # Обновляем склад
                    cursor.execute(
                        """INSERT INTO stock (product_id, name, volume, strength, quantity, price) 
                           VALUES (%s, %s, %s, %s, %s, %s) 
                           ON DUPLICATE KEY UPDATE 
                           quantity = quantity + VALUES(quantity), 
                           price = VALUES(price)""",
                        (product_id, name, volume, strength, quantity, total_price)
                    )

                    # Обновляем статус поставки для этого товара
                    cursor.execute(
                        "UPDATE transactions SET status='received' WHERE purchase_id=%s AND product_id=%s",
                        (selected_purchase_id, product_id))

                conn.commit()
                print("Поставка принята!")
                receive_window.destroy()

        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")

    def write_off_goods(self):
        # Логика списания брака
        pass

    def stock_report(self):
        # Логика отчета по складу
        pass


if __name__ == "__main__":
    app = StorekeeperDashboard()
    app.mainloop()
