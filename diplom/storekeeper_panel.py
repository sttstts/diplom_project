import customtkinter as ctk
import tkinter as tk
import pymysql
import re
from tkinter import W, CENTER, E
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from logger import log_action
from barcodes import generate_barcodes_for_batch
import os

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"


class StorekeeperDashboard(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Окно кладовщика")
        self.geometry("100x100")
        self.center_window(700, 350)
        self.resizable(False, False)

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

    def logout(self):
        self.destroy()
        from login import LoginApp
        login_window = LoginApp()
        login_window.mainloop()

    def check_barcode(self):
        def submit():
            barcode_value = entry_barcode.get().strip()
            if not barcode_value:
                result_label.configure(text="Введите штрих-код!", text_color="red")
                return

            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
                cursor = conn.cursor()

                query = """
                    SELECT 
                        b.batch_id,
                        b.product_id,
                        b.bottle_id,
                        b.barcode,
                        p.name,
                        p.volume,
                        p.strength,
                        p.price
                    FROM barcodes b
                    JOIN products p ON b.product_id = p.id
                    WHERE b.barcode = %s
                """
                cursor.execute(query, (barcode_value,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    batch_id, product_id, bottle_id, barcode, name, volume, strength, price = result
                    result_text = (
                        f"Продукция легальна!\n\n"
                        f"Название: {name}\n"
                        f"Номер партии: {batch_id}\n"
                        f"ID бутылки: {bottle_id}\n"
                        f"Объём: {volume} л\n"
                        f"Крепость: {strength}°\n"
                        f"Цена: {price:.2f} руб.\n"
                        f"Штрихкод: {barcode}"
                    )
                    result_label.configure(text=result_text, text_color="green")
                    log_action(self.username, f"Проверил штрих-код {barcode_value}: продукция легальна")
                else:
                    result_label.configure(text="Штрих-код не найден в базе!", text_color="red")
                    log_action(self.username, f"Проверил штрих-код {barcode_value}: не найден")
            except pymysql.MySQLError as e:
                result_label.configure(text=f"Ошибка БД: {e}", text_color="red")

        barcode_window = ctk.CTkToplevel(self)
        barcode_window.title("Проверка в ЕГАИС")
        barcode_window.geometry("400x350")
        barcode_window.transient(self)
        barcode_window.grab_set()
        barcode_window.focus_set()

        ctk.CTkLabel(barcode_window, text="Введите или сканируйте штрих-код:").pack(pady=5)
        entry_barcode = ctk.CTkEntry(barcode_window)
        entry_barcode.pack(pady=5)

        ctk.CTkButton(barcode_window, text="Проверить", command=submit).pack(pady=10)

        result_label = ctk.CTkLabel(barcode_window, text="", justify="left", wraplength=360)
        result_label.pack(pady=10)

    def stock_report(self):
        filename = f"Отчет_по_складу_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        report_dir = r"C:\Users\Степан\PycharmProjects\diplom\отчёты\склдаской отчёт"
        filepath = os.path.join(report_dir, filename)

        pdfmetrics.registerFont(TTFont('DejaVu', r'C:\Users\Степан\PycharmProjects\diplom\font\DejaVuSans.ttf'))

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        c.setFont("DejaVu", 16)
        c.drawString(200, height - 50, "Отчет по складу")

        c.setFont("DejaVu", 12)
        report_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        c.drawString(200, height - 70, f"Дата создания: {report_date}")

        data = [["Название", "Объём", "Крепкость", "Количество", "Цена (р)"]]
        with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, volume, strength, quantity, price FROM stock")
            items = cursor.fetchall()

        for item in items:
            data.append([item[0], item[1], item[2], item[3], f"{item[4]:.2f} р"])

        col_widths = [max(len(str(row[i])) for row in data) * 8 for i in range(len(data[0]))]
        col_widths = [min(w, 150) for w in col_widths]

        table = Table(data, colWidths=col_widths)

        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        table_width = sum(col_widths)
        if table_width > width - 100:
            scale_factor = (width - 100) / table_width
            table._argW = [w * scale_factor for w in col_widths]

        row_height = 20
        start_y = height - 120
        available_height = start_y - 50
        rows_per_page = int(available_height // row_height)

        header = data[0]
        rows = data[1:]

        current_y = start_y

        for i in range(0, len(rows), rows_per_page):
            page_rows = rows[i:i + rows_per_page]
            page_data = [header] + page_rows

            table = Table(page_data, colWidths=col_widths)
            table.setStyle(style)

            table.wrapOn(c, width, height)
            table.drawOn(c, 50, current_y - (len(page_data) * row_height))

            if i + rows_per_page < len(rows):
                c.showPage()
                c.setFont("DejaVu", 16)
                c.drawString(200, height - 50, "Отчет по складу")
                c.setFont("DejaVu", 12)
                c.drawString(200, height - 70, f"Дата создания: {report_date}")
                current_y = height - 120

        c.save()

        log_action(self.username, f"Создал отчет по складу: {filename}")
        print(f"PDF-отчёт создан: {filepath}")

    def view_stock(self):
        stock_window = ctk.CTkToplevel(self)
        stock_window.title("Склад")
        stock_window.geometry("815x500")

        stock_window.transient(self)
        stock_window.grab_set()
        stock_window.focus_set()

        header_frame = ctk.CTkFrame(stock_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        columns = ["ID", "Наименование", "Объем (L)", "Крепость (%)", "Количество (шт)", "Цена"]
        widths = [50, 200, 100, 100, 100, 100]

        for i, col in enumerate(columns):
            ctk.CTkLabel(header_frame, text=col, width=widths[i], anchor="w").grid(row=0, column=i, padx=10, pady=5, sticky="w")

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

            for j, value in enumerate(item):
                text = f"{value:.2f} руб." if j == 5 else str(value)
                ctk.CTkLabel(row_frame, text=text, width=widths[j], anchor="w").grid(row=0, column=j, padx=10, pady=2, sticky="w")

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        log_action(self.username, "Просмотрел склад")

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        stock_window.bind_all("<MouseWheel>", on_mouse_wheel)

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

        self.complete_button = None

        deliveries_dropdown.configure(
            command=lambda value: self.show_items(value, receive_window))

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

                if self.complete_button:
                    self.complete_button.destroy()
                    self.complete_button = None

                self.complete_button = ctk.CTkButton(receive_window, text="Завершить приём поставки",
                                                     command=lambda: self.accept_delivery(selected_delivery_id,
                                                                                          receive_window))
                self.complete_button.pack(pady=20)

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
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )

            with connection:
                cursor = connection.cursor()

                for product_id, quantity in selected_items:
                    cursor.execute("SELECT name, volume, strength, price FROM products WHERE id=%s", (product_id,))
                    result = cursor.fetchone()
                    if result is None:
                        print(f"Продукт с id={product_id} не найден")
                        continue

                    name = result['name']
                    volume = result['volume']
                    strength = result['strength']
                    unit_price = result['price']

                    try:
                        volume = float(volume) if volume is not None else 1.0
                        strength = float(strength) if strength is not None else 1.0
                    except ValueError:
                        volume = 1.0
                        strength = 1.0

                    total_price = float(unit_price) * int(quantity)

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
                        (selected_purchase_id, product_id)
                    )

                generate_barcodes_for_batch(selected_purchase_id, connection)

                connection.commit()
                log_action(self.username, f"Принял поставку #{selected_purchase_id}")
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

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        write_off_window.bind_all("<MouseWheel>", on_mouse_wheel)

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

        barcode_label = ctk.CTkLabel(write_off_detail_window, text="Введите штрихкод для списания:")
        barcode_label.pack(padx=10, pady=5)

        barcode_entry = ctk.CTkEntry(write_off_detail_window)
        barcode_entry.pack(padx=10, pady=5)

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

        confirm_button = ctk.CTkButton(
            write_off_detail_window,
            text="Подтвердить списание",
            command=lambda: self.confirm_write_off(item, barcode_entry, reason_var, write_off_detail_window)
        )
        confirm_button.pack(padx=10, pady=20)

    def confirm_write_off(self, item, barcode_entry, reason_var, write_off_detail_window):
        if hasattr(self, "write_off_error_label"):
            self.write_off_error_label.destroy()

        barcode = barcode_entry.get().strip()
        reason = reason_var.get()

        if not barcode or len(barcode.split("-")) != 3:
            self.write_off_error_label = ctk.CTkLabel(write_off_detail_window,
                                                      text="Неверный формат штрихкода (ожидается XXX-XXX-XXX)")
            self.write_off_error_label.pack(padx=10, pady=5)
            return

        if not reason:
            self.write_off_error_label = ctk.CTkLabel(write_off_detail_window,
                                                      text="Пожалуйста, выберите причину списания")
            self.write_off_error_label.pack(padx=10, pady=5)
            return

        try:
            batch_id_str, product_id_str, bottle_id_str = barcode.split("-")
            batch_id = int(batch_id_str)
            product_id = int(product_id_str)
            bottle_id = int(bottle_id_str)

            with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT product_id FROM stock WHERE id = %s", (item[0],))
                stock_product_result = cursor.fetchone()
                if not stock_product_result:
                    self.write_off_error_label = ctk.CTkLabel(write_off_detail_window, text="Товар не найден в базе")
                    self.write_off_error_label.pack(padx=10, pady=5)
                    return

                stock_product_id = stock_product_result[0]

                if product_id != stock_product_id:
                    self.write_off_error_label = ctk.CTkLabel(write_off_detail_window,
                                                              text="Штрихкод не соответствует выбранному товару")
                    self.write_off_error_label.pack(padx=10, pady=5)
                    return

                cursor.execute(
                    "SELECT id FROM barcodes WHERE product_id=%s AND bottle_id=%s AND batch_id=%s",
                    (product_id, bottle_id, batch_id)
                )
                barcode_record = cursor.fetchone()

                if not barcode_record:
                    self.write_off_error_label = ctk.CTkLabel(write_off_detail_window, text="Штрихкод не найден в базе")
                    self.write_off_error_label.pack(padx=10, pady=5)
                    return

                cursor.execute("DELETE FROM barcodes WHERE id = %s", (barcode_record[0],))

                cursor.execute("UPDATE stock SET quantity = quantity - 1 WHERE id = %s", (item[0],))

                cursor.execute("DELETE FROM stock WHERE quantity <= 0")

                conn.commit()

                log_action(self.username, f"Списал товар '{item[1]}' (штрихкод: {barcode}) по причине: {reason}")
                write_off_detail_window.destroy()

        except ValueError:
            self.write_off_error_label = ctk.CTkLabel(write_off_detail_window,
                                                      text="Некорректный формат чисел в штрихкоде")
            self.write_off_error_label.pack(padx=10, pady=5)
        except pymysql.MySQLError as e:
            self.write_off_error_label = ctk.CTkLabel(write_off_detail_window, text=f"Ошибка базы данных: {e}")
            self.write_off_error_label.pack(padx=10, pady=5)


if __name__ == "__main__":
    app = StorekeeperDashboard()
    app.mainloop()
