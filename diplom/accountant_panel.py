import os
import pymysql
import customtkinter as ctk
from tkinter import W, CENTER, E, messagebox
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from logger import log_action



DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AccountantDashboard(ctk.CTk):
    def __init__(self, username,cart=None):
        super().__init__()
        self.username = username
        self.title("Окно бухгалтера")
        self.geometry("700x350")
        self.center_window(700, 350)
        self.resizable(False, False)

        self.validate_50 = self.register(self.limit_50_chars)

        self.cart = cart if cart is not None else []

        self.purchase_goods_btn = self.create_tile_button("Закупка товара", self.purchase_goods)
        self.purchase_goods_btn.place(relx=0.15, rely=0.25, anchor=W)

        self.sell_goods_btn = self.create_tile_button("Продажа товара", self.sell_goods)
        self.sell_goods_btn.place(relx=0.7, rely=0.25, anchor=CENTER)

        self.financial_report_btn = self.create_tile_button("Финансовый отчет", self.financial_report)
        self.financial_report_btn.place(relx=0.15, rely=0.65, anchor=W)

        self.logout_btn = self.create_tile_button("Выход", self.logout)
        self.logout_btn.place(relx=0.7, rely=0.65, anchor=CENTER)

    def create_tile_button(self, text, command):
        button = ctk.CTkButton(self, text=text, command=command, width=220, height=120, corner_radius=15,
                               fg_color="#3b8ed0", hover_color="#2971a4", font=('', 20))
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
        if self.winfo_exists():
            self.destroy()

        from login import LoginApp
        login_window = LoginApp()
        login_window.mainloop()

    def purchase_goods(self):
        purchase_window = ctk.CTkToplevel(self)
        purchase_window.title("Закупка товара")
        purchase_window.geometry("500x400")
        purchase_window.transient(self)
        purchase_window.grab_set()
        purchase_window.focus_set()

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        products = cursor.fetchall()
        conn.close()

        if not products:
            messagebox.showinfo("ошибка", "В базе данных нет товаров.")
            return

        self.product_dict = {f"{p[1]} (Цена: {p[2]})": {"id": p[0], "name": p[1], "price": p[2]} for p in products}

        self.selected_product = ctk.StringVar(value=list(self.product_dict.keys())[0])

        def update_selected_product(choice):
            self.selected_product.set(choice)

        product_dropdown = ctk.CTkComboBox(
            purchase_window, values=list(self.product_dict.keys()), variable=self.selected_product,
            command=update_selected_product
        )
        product_dropdown.pack(pady=5)

        ctk.CTkLabel(purchase_window, text="Количество:").pack()
        entry_quantity = ctk.CTkEntry(purchase_window)
        entry_quantity.pack()

        cart_listbox = ctk.CTkTextbox(purchase_window, height=100)
        cart_listbox.pack()

        total_price_label = ctk.CTkLabel(purchase_window, text="Итоговая сумма: 0.00 руб.")
        total_price_label.pack(pady=5)

        def update_cart_total():
            total = 0
            for item in self.cart:
                total += item["quantity"] * float(item["price"])
            total_price_label.configure(text=f"Итоговая сумма: {total:.2f} руб.")

        def add_to_cart():
            selected = self.selected_product.get().strip()
            quantity = entry_quantity.get().strip()

            if not selected:
                messagebox.showinfo("Ошибка", "Не выбран товар.")
                return

            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showinfo("Ошибка", "Введите корректное количество.")
                return

            product_data = self.product_dict.get(selected)

            if product_data:
                self.cart.append({"id": product_data["id"], "name": product_data["name"],
                                  "price": product_data["price"], "quantity": int(quantity)})

                cart_listbox.insert("end", f"{product_data['name']} - {quantity} шт.\n")

                entry_quantity.delete(0, "end")

                update_cart_total()
            else:
                messagebox.showinfo("Ошибка", "Товар не найден.")

        ctk.CTkButton(purchase_window, text="Добавить в корзину", command=add_to_cart).pack(pady=5)

        def purchase():
            if not self.cart:
                messagebox.showinfo("Ошибка", "Корзина пуста, невозможно выполнить покупку.")
                return

            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO purchases (purchase_date) VALUES (NOW())")
            purchase_id = cursor.lastrowid

            for item in self.cart:
                product_id = item["id"]
                quantity = item["quantity"]
                total_price = item["quantity"] * item["price"]

                cursor.execute(
                    "INSERT INTO transactions (transaction_type, product_id, quantity, total_price, status, purchase_id) "
                    "VALUES ('purchase', %s, %s, %s, 'pending', %s)",
                    (product_id, quantity, total_price, purchase_id)
                )

            conn.commit()
            conn.close()
            self.cart.clear()
            cart_listbox.delete("1.0", "end")
            update_cart_total()
            messagebox.showinfo("Успех", "Закупка успешно проведена! Ожидает подтверждения кладовщика.")
            log_action(self.username,
                       f"Бухгалтер {self.username} выполнил(а) закупку товаров (покупка ID: {purchase_id})")

        ctk.CTkButton(purchase_window, text="Закупить", command=purchase).pack(pady=5)

    def sell_goods(self):
        sell_window = ctk.CTkToplevel(self)
        sell_window.title("Продажа товара")
        sell_window.geometry("500x400")
        sell_window.transient(self)
        sell_window.grab_set()
        sell_window.focus_set()

        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT products.id, products.name, products.price, stock.quantity FROM products JOIN stock ON stock.product_id = products.id;")
        products = cursor.fetchall()
        conn.close()

        if not products:
            messagebox.showinfo("Ошибка", "В базе данных нет товаров!")
            return

        self.product_dict = {
            f"{p[1]} (Остаток: {p[3]} шт., Цена: {p[2]})": {"id": p[0], "name": p[1], "price": p[2], "stock": p[3]}
            for p in products
        }

        self.selected_product = ctk.StringVar(value=list(self.product_dict.keys())[0])

        def update_selected_product(choice):
            self.selected_product.set(choice)
            product_data = self.product_dict[choice]
            price_entry.delete(0, "end")
            price_entry.insert(0, str(product_data["price"]))
            update_total_price()

        ctk.CTkLabel(sell_window, text="Выберите товар:").pack()
        product_dropdown = ctk.CTkComboBox(
            sell_window, values=list(self.product_dict.keys()), variable=self.selected_product,
            command=update_selected_product
        )
        product_dropdown.pack(pady=5)

        ctk.CTkLabel(sell_window, text="Количество:").pack()
        quantity_entry = ctk.CTkEntry(sell_window)
        quantity_entry.pack()

        ctk.CTkLabel(sell_window, text="Цена за единицу:").pack()
        price_entry = ctk.CTkEntry(sell_window, validate="key", validatecommand=(self.validate_50, "%P"))
        price_entry.pack()

        total_price_label = ctk.CTkLabel(sell_window, text="Итоговая сумма: 0.00")
        total_price_label.pack()

        def update_total_price(*args):
            selected = self.selected_product.get()
            product_data = self.product_dict[selected]

            try:
                quantity = int(quantity_entry.get())
                price_per_unit = float(price_entry.get())
                total_price = quantity * price_per_unit
                total_price_label.configure(text=f"Итоговая сумма: {total_price:.2f} руб.")
            except ValueError:
                total_price_label.configure(text="Итоговая сумма: 0.00")

        quantity_entry.bind("<KeyRelease>", update_total_price)
        price_entry.bind("<KeyRelease>", update_total_price)

        def process_sale():
            selected = self.selected_product.get()
            product_data = self.product_dict[selected]

            quantity = quantity_entry.get().strip()
            price_per_unit = price_entry.get().strip()

            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showinfo("Ошибка", "Введите корректное количество.")
                return

            quantity = int(quantity)
            price_per_unit = float(price_per_unit)

            if quantity > product_data["stock"]:
                messagebox.showinfo("Ошибка", "недостаточно товаров на складе.")
                return

            total_price = quantity * price_per_unit

            try:
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, barcode FROM barcodes
                    WHERE product_id = %s
                    ORDER BY id ASC
                    LIMIT %s
                """, (product_data["id"], quantity))
                barcode_rows = cursor.fetchall()

                if len(barcode_rows) < quantity:
                    messagebox.showinfo("Ошибка", "Недостаточно штрихкодов для этого товара.")
                    conn.close()
                    return

                barcode_ids = [row[0] for row in barcode_rows]
                barcode_list = [row[1] for row in barcode_rows]

                format_strings = ','.join(['%s'] * len(barcode_ids))
                cursor.execute(f"DELETE FROM barcodes WHERE id IN ({format_strings})", barcode_ids)

                cursor.execute(
                    "INSERT INTO transactions (transaction_type, product_id, quantity, total_price, status, sale_date) "
                    "VALUES ('sale', %s, %s, %s, 'completed', NOW())",
                    (product_data["id"], quantity, total_price)
                )

                cursor.execute(
                    "UPDATE stock SET quantity = quantity - %s WHERE product_id = %s",
                    (quantity, product_data["id"])
                )

                cursor.execute(
                    "DELETE FROM stock WHERE product_id = %s AND quantity <= 0",
                    (product_data["id"],)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Успех", f"Товар продан: {product_data['name']} - {quantity} шт. по {price_per_unit} руб. Итог: {total_price} руб.")
                log_action(self.username,
                           f"Бухгалтер {self.username} продал(а) товар: {product_data['name']} - {quantity} шт. по {price_per_unit} руб. Итог: {total_price} руб.")

                result_window = ctk.CTkToplevel(self)
                result_window.title("Продажа завершена")
                result_window.geometry("400x300")
                result_window.transient(self)
                result_window.grab_set()

                ctk.CTkLabel(result_window, text=f"Продан товар: {product_data['name']}").pack(pady=5)
                ctk.CTkLabel(result_window, text=f"Количество: {quantity} шт.").pack(pady=5)
                ctk.CTkLabel(result_window, text="Списанные штрихкоды:").pack(pady=5)

                scroll_frame = ctk.CTkScrollableFrame(result_window, height=180, width=360)
                scroll_frame.pack(padx=10, pady=5, fill="both", expand=False)

                text_box = ctk.CTkTextbox(scroll_frame, width=320)
                text_box.pack(padx=5, pady=5, fill="both", expand=True)

                text_box.configure(state="normal")
                text_box.insert("1.0", '\n'.join(barcode_list))
                text_box.configure(state="disabled")

                def close_all():
                    result_window.destroy()
                    sell_window.destroy()

                ctk.CTkButton(result_window, text="Закрыть", command=close_all).pack(pady=10)


            except pymysql.MySQLError as e:
                messagebox.showinfo("Ошибка", f"Ошибка базы данных: {e}")

        ctk.CTkButton(sell_window, text="Продать", command=process_sale).pack(pady=10)

    def financial_report(self):
        report_window = ctk.CTkToplevel(self)
        report_window.title("Финансовый отчет")
        report_window.geometry("1090x500")
        report_window.transient(self)
        report_window.grab_set()
        report_window.focus_set()

        self.sort_type_state = None
        self.sort_total_state = None
        self.sort_quantity_state = None
        self.sort_name_state = None
        self.sort_date_state = None

        header_frame = ctk.CTkFrame(report_window)
        header_frame.pack(fill="x", padx=10, pady=5)

        widths = [100, 200, 100, 150, 150]

        def toggle_sort_type():
            if self.sort_type_state is None:
                self.sort_type_state = "asc"
            elif self.sort_type_state == "asc":
                self.sort_type_state = "desc"
            else:
                self.sort_type_state = None
            self.sort_total_state = None
            self.sort_quantity_state = None
            self.sort_name_state = None
            self.sort_date_state = None
            load_transactions()

        def toggle_sort_total():
            if self.sort_total_state is None:
                self.sort_total_state = "asc"
            elif self.sort_total_state == "asc":
                self.sort_total_state = "desc"
            else:
                self.sort_total_state = None
            self.sort_type_state = None
            self.sort_quantity_state = None
            self.sort_name_state = None
            self.sort_date_state = None
            load_transactions()

        def toggle_sort_quantity():
            if self.sort_quantity_state is None:
                self.sort_quantity_state = "asc"
            elif self.sort_quantity_state == "asc":
                self.sort_quantity_state = "desc"
            else:
                self.sort_quantity_state = None
            self.sort_type_state = None
            self.sort_total_state = None
            self.sort_name_state = None
            self.sort_date_state = None
            load_transactions()

        def toggle_sort_name():
            if self.sort_name_state is None:
                self.sort_name_state = "asc"
            elif self.sort_name_state == "asc":
                self.sort_name_state = "desc"
            else:
                self.sort_name_state = None
            self.sort_type_state = None
            self.sort_total_state = None
            self.sort_quantity_state = None
            self.sort_date_state = None
            load_transactions()

        def toggle_sort_date():
            if self.sort_date_state is None:
                self.sort_date_state = "desc"
            elif self.sort_date_state == "desc":
                self.sort_date_state = "asc"
            else:
                self.sort_date_state = None
            self.sort_type_state = None
            self.sort_total_state = None
            self.sort_quantity_state = None
            self.sort_name_state = None
            load_transactions()

        ctk.CTkButton(header_frame, text="Тип ⬍", width=widths[0], command=toggle_sort_type).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(header_frame, text="Наименование ⬍", width=widths[1], command=toggle_sort_name).grid(
            row=0, column=1, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(header_frame, text="Кол-во ⬍", width=widths[2], command=toggle_sort_quantity).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(header_frame, text="Сумма (руб) ⬍", width=widths[3], command=toggle_sort_total).grid(
            row=0, column=3, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(header_frame, text="Дата ⬍", width=widths[4], command=toggle_sort_date).grid(
            row=0, column=4, padx=10, pady=5, sticky="w"
        )

        # --- Добавляем фильтры ---
        search_name = ctk.CTkEntry(header_frame, placeholder_text="Поиск по наименованию")
        search_name.grid(row=1, column=0, padx=10, pady=5, sticky="w", columnspan=2)

        date_from_entry = ctk.CTkEntry(header_frame, placeholder_text="Дата от (ГГГГ-ММ-ДД)")
        date_from_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        date_to_entry = ctk.CTkEntry(header_frame, placeholder_text="Дата до (ГГГГ-ММ-ДД)")
        date_to_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        def apply_filters():
            load_transactions()

        ctk.CTkButton(header_frame, text="Поиск", command=apply_filters).grid(row=1, column=4, padx=10, pady=5,
                                                                              sticky="w")
        # ---------------------------

        report_canvas = ctk.CTkCanvas(report_window)
        report_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(report_window, orientation="vertical", command=report_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        report_canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(report_canvas)
        report_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.update_idletasks()

        global summary_frame
        summary_frame = ctk.CTkFrame(report_window)
        summary_frame.pack(fill="x", padx=10, pady=10)

        def load_transactions():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            for widget in summary_frame.winfo_children():
                widget.destroy()

            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            # Получаем фильтры из полей
            name_filter = search_name.get().strip()
            date_from = date_from_entry.get().strip()
            date_to = date_to_entry.get().strip()

            filters = []
            params = []

            if name_filter:
                filters.append("p.name LIKE %s")
                params.append(f"%{name_filter}%")

            if date_from:
                filters.append(
                    """(IFNULL(t.sale_date, (SELECT purchase_date FROM purchases WHERE purchases.id = t.purchase_id)) >= %s)""")
                params.append(date_from)

            if date_to:
                filters.append(
                    """(IFNULL(t.sale_date, (SELECT purchase_date FROM purchases WHERE purchases.id = t.purchase_id)) <= %s)""")
                params.append(date_to)

            where_clause = " AND ".join(filters)
            if where_clause:
                where_clause = " AND " + where_clause

            # Определяем порядок сортировки
            if self.sort_date_state is not None:
                direction = "DESC" if self.sort_date_state == "desc" else "ASC"
                order_clause = f"ORDER BY t.sale_date {direction}"
            elif self.sort_type_state is not None:
                direction = "ASC" if self.sort_type_state == "asc" else "DESC"
                order_clause = f"ORDER BY t.transaction_type {direction}"
            elif self.sort_name_state is not None:
                direction = "ASC" if self.sort_name_state == "asc" else "DESC"
                order_clause = f"ORDER BY p.name {direction}"
            elif self.sort_total_state is not None:
                direction = "ASC" if self.sort_total_state == "asc" else "DESC"
                order_clause = f"ORDER BY t.total_price {direction}"
            elif self.sort_quantity_state is not None:
                direction = "ASC" if self.sort_quantity_state == "asc" else "DESC"
                order_clause = f"ORDER BY t.quantity {direction}"
            else:
                order_clause = "ORDER BY date ASC"

            cursor.execute(f"""
                SELECT t.transaction_type, p.name, t.quantity, t.total_price, 
                       IFNULL(t.sale_date, (SELECT purchase_date FROM purchases WHERE purchases.id = t.purchase_id)) as date
                FROM transactions t
                LEFT JOIN products p ON t.product_id = p.id
                WHERE (t.status = 'completed' OR t.transaction_type = 'purchase')
                {where_clause}
                {order_clause};
            """, params)

            transactions = cursor.fetchall()
            conn.close()

            total_income = 0
            total_expense = 0

            for trans_type, name, quantity, total, date in transactions:
                row_frame = ctk.CTkFrame(scrollable_frame)
                row_frame.pack(fill="x", padx=10, pady=2)

                trans_type_display = "Продажа" if trans_type == "sale" else "Закупка"
                total_display = f"{total:.2f} руб."
                date_display = date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(date, datetime) else str(date)

                values = [trans_type_display, name, quantity, total_display, date_display]

                for j, value in enumerate(values):
                    ctk.CTkLabel(row_frame, text=str(value), width=widths[j], anchor="w").grid(
                        row=0, column=j, padx=10, pady=2, sticky="w"
                    )

                if trans_type == "sale":
                    total_income += total
                elif trans_type == "purchase":
                    total_expense += total

            scrollable_frame.update_idletasks()
            report_canvas.config(scrollregion=report_canvas.bbox("all"))

            for widget in summary_frame.winfo_children():
                widget.destroy()

            ctk.CTkLabel(summary_frame, text=f"Общий доход: {total_income:.2f} руб.", anchor="w").pack(anchor="w",
                                                                                                       padx=10, pady=2)
            ctk.CTkLabel(summary_frame, text=f"Общие расходы: {total_expense:.2f} руб.", anchor="w").pack(anchor="w",
                                                                                                          padx=10,
                                                                                                          pady=2)
            ctk.CTkLabel(summary_frame, text=f"Итоговая прибыль: {total_income - total_expense:.2f} руб.",
                         anchor="w").pack(anchor="w", padx=10, pady=2)

        def on_mouse_wheel(event):
            report_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        report_window.bind_all("<MouseWheel>", on_mouse_wheel)

        load_transactions()

        def generate_pdf_report():
            filename = f"Финансовый_отчет_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
            report_dir = r"C:\Users\Степан\PycharmProjects\diplom\отчёты\финансовые отчёты"
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)
            filepath = os.path.join(report_dir, filename)

            pdfmetrics.registerFont(TTFont('DejaVu', r'C:\Users\Степан\PycharmProjects\diplom\font\DejaVuSans.ttf'))

            doc = SimpleDocTemplate(filepath, pagesize=A4,
                                    rightMargin=30, leftMargin=30,
                                    topMargin=30, bottomMargin=30)

            styles = getSampleStyleSheet()
            styles["Normal"].fontName = "DejaVu"
            styles["Heading1"].fontName = "DejaVu"

            elements = []

            elements.append(Paragraph("Финансовый отчет", styles['Heading1']))
            elements.append(Spacer(1, 12))
            report_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            elements.append(Paragraph(f"Дата создания: {report_date}", styles['Normal']))
            elements.append(Spacer(1, 12))

            data = [["Тип", "Наименование", "Кол-во", "Сумма (руб)", "Дата"]]

            with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT t.transaction_type, p.name, t.quantity, t.total_price, 
                           IFNULL(t.sale_date, (SELECT purchase_date FROM purchases WHERE purchases.id = t.purchase_id)) as date
                    FROM transactions t
                    LEFT JOIN products p ON t.product_id = p.id
                    WHERE t.status = 'completed' OR t.transaction_type = 'purchase'
                """)
                transactions = cursor.fetchall()

            for trans_type, name, quantity, total, date in transactions:
                trans_type_display = "Продажа" if trans_type == "sale" else "Закупка"
                date_display = date.strftime("%d.%m.%Y %H:%M:%S")
                data.append([trans_type_display, name, quantity, f"{total:.2f} руб", date_display])

            col_widths = [80, 150, 60, 80, 120]

            table = Table(data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            elements.append(table)

            doc.build(elements)

            messagebox.showinfo("Успех", f"PDF-отчёт создан: {filepath}")
            log_action(self.username, f"Бухгалтер {self.username} создал финансовый отчёт")

        load_transactions()

        ctk.CTkButton(report_window, text="Создать PDF-отчёт", command=generate_pdf_report).pack(pady=10)

    def limit_50_chars(self, new_value):
        return len(new_value) <= 50

if __name__ == "__main__":
    app = AccountantDashboard()
    app.mainloop()
