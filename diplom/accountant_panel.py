import customtkinter as ctk
import pymysql
import datetime
from tkinter import W, CENTER, E

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AccountantDashboard(ctk.CTk):
    def __init__(self, cart=None):
        super().__init__()
        self.title("Окно бухгалтера")
        self.geometry("700x350")
        self.center_window(700, 350)
        self.resizable(False, False)

        self.cart = cart if cart is not None else []

        button_width = 200
        button_height = 120
        padding = 20

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
            print("Ошибка: в базе данных нет товаров!")
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

        def add_to_cart():
            selected = self.selected_product.get().strip()
            quantity = entry_quantity.get().strip()

            print(f"Выбранный товар: '{selected}'")
            print(f"Доступные товары: {list(self.product_dict.keys())}")

            if not selected:
                print("Ошибка: не выбран товар!")
                return

            if not quantity.isdigit() or int(quantity) <= 0:
                print("Ошибка: введите корректное количество!")
                return

            product_data = self.product_dict.get(selected)

            if product_data:
                self.cart.append({"id": product_data["id"], "name": product_data["name"],
                                  "price": product_data["price"], "quantity": int(quantity)})

                cart_listbox.insert("end", f"{product_data['name']} - {quantity} шт.\n")
                print(f"Товар добавлен в корзину: {product_data['name']} - {quantity} шт.")
            else:
                print("Ошибка: товар не найден!")

        ctk.CTkButton(purchase_window, text="Добавить в корзину", command=add_to_cart).pack(pady=5)

        def purchase():
            if not self.cart:
                print("Корзина пуста, невозможно выполнить закупку!")
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
            print("Закупка успешно проведена! Ожидает подтверждения кладовщика.")

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
            print("Ошибка: в базе данных нет товаров!")
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
        price_entry = ctk.CTkEntry(sell_window)
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
                print("Ошибка: введите корректное количество!")
                return

            quantity = int(quantity)
            price_per_unit = float(price_per_unit)

            if quantity > product_data["stock"]:
                print("Ошибка: недостаточно товара на складе!")
                return

            total_price = quantity * price_per_unit

            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO transactions (transaction_type, product_id, quantity, total_price, status, sale_date) "
                "VALUES ('sale', %s, %s, %s, 'completed', NOW())",
                (product_data["id"], quantity, total_price)
            )

            cursor.execute(
                "UPDATE stock SET quantity = quantity - %s WHERE product_id = %s",
                (quantity, product_data["id"])
            )

            conn.commit()
            conn.close()

            print(
                f"Продан товар: {product_data['name']} - {quantity} шт. по {price_per_unit} руб. Итог: {total_price} руб."
            )

            sell_window.destroy()

        ctk.CTkButton(sell_window, text="Продать", command=process_sale).pack(pady=10)

    def financial_report(self):
        pass


if __name__ == "__main__":
    app = AccountantDashboard()
    app.mainloop()
