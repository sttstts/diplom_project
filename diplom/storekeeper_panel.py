import customtkinter as ctk
import pymysql
import random

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class StorekeeperDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Окно кладовщика")
        self.geometry("600x400")

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

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM stock")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            ctk.CTkLabel(stock_window, text=f"{item[0]}. {item[1]} - {item[2]} шт.").pack()

    def receive_goods(self):
        receive_window = ctk.CTkToplevel(self)
        receive_window.title("Приём поставок")
        receive_window.geometry("500x400")
        receive_window.transient(self)
        receive_window.grab_set()
        receive_window.focus_set()

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, product_id, quantity FROM transactions WHERE transaction_type='purchase' AND status='pending'")
        pending_deliveries = cursor.fetchall()

        if not pending_deliveries:
            ctk.CTkLabel(receive_window, text="Нет ожидающих поставок").pack()
            return

        deliveries_dict = {}
        transaction_ids = set()
        for p in pending_deliveries:
            transaction_id = p[0]
            product_id = p[1]
            cursor.execute("SELECT name FROM products WHERE id=%s", (product_id,))
            product_name = cursor.fetchone()[0]

            if transaction_id not in deliveries_dict:
                deliveries_dict[transaction_id] = []

            deliveries_dict[transaction_id].append((f"{product_name} - {p[2]} шт.", p[0]))
            transaction_ids.add(transaction_id)

        self.deliveries_checkbox_list = []
        for transaction_id in transaction_ids:
            delivery_items = deliveries_dict[transaction_id]
            for item, trans_id in delivery_items:
                checkbox = ctk.CTkCheckBox(receive_window, text=item, onvalue=trans_id, offvalue=0)
                self.deliveries_checkbox_list.append(checkbox)
                checkbox.pack(anchor="w")

        def accept_delivery():
            selected_items = [checkbox.get() for checkbox in self.deliveries_checkbox_list if checkbox.get() != 0]
            if not selected_items:
                ctk.CTkLabel(receive_window, text="Не выбраны товары для приёма").pack()
                return

            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
                cursor = conn.cursor()

                for transaction_id in selected_items:
                    cursor.execute("UPDATE transactions SET status='received' WHERE id=%s", (transaction_id,))

                    cursor.execute("SELECT product_id, quantity FROM transactions WHERE id=%s", (transaction_id,))
                    product_id, quantity = cursor.fetchone()

                    cursor.execute(
                        "INSERT INTO stock (product_id, quantity) VALUES (%s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + %s",
                        (product_id, quantity, quantity))

                conn.commit()
                print("Поставка принята!")
                receive_window.destroy()

            except pymysql.MySQLError as e:
                print(f"Ошибка MySQL: {e}")

            finally:
                if conn:
                    conn.close()

        ctk.CTkButton(receive_window, text="Завершить приём поставки", command=accept_delivery).pack(pady=10)

    def write_off_goods(self):
        def submit():
            stock_id = int(entry_id.get())
            quantity = int(entry_quantity.get())
            reason = entry_reason.get()

            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE stock SET quantity = quantity - %s WHERE id = %s", (quantity, stock_id))
            cursor.execute("INSERT INTO write_offs (stock_id, quantity, reason) VALUES (%s, %s, %s)",
                           (stock_id, quantity, reason))
            conn.commit()
            conn.close()
            write_off_window.destroy()

        write_off_window = ctk.CTkToplevel(self)
        write_off_window.title("Списание брака")
        write_off_window.geometry("300x250")
        write_off_window.transient(self)
        write_off_window.grab_set()
        write_off_window.focus_set()

        ctk.CTkLabel(write_off_window, text="ID товара:").pack()
        entry_id = ctk.CTkEntry(write_off_window)
        entry_id.pack()

        ctk.CTkLabel(write_off_window, text="Количество:").pack()
        entry_quantity = ctk.CTkEntry(write_off_window)
        entry_quantity.pack()

        ctk.CTkLabel(write_off_window, text="Причина:").pack()
        entry_reason = ctk.CTkEntry(write_off_window)
        entry_reason.pack()

        ctk.CTkButton(write_off_window, text="Списать", command=submit).pack(pady=10)

    def stock_report(self):
        report_window = ctk.CTkToplevel(self)
        report_window.title("Отчет по складу")
        report_window.geometry("400x300")
        report_window.transient(self)
        report_window.grab_set()
        report_window.focus_set()

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, SUM(quantity) FROM stock GROUP BY name")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            ctk.CTkLabel(report_window, text=f"{item[0]}: {item[1]} шт.").pack()

if __name__ == "__main__":
    app = StorekeeperDashboard()
    app.mainloop()
