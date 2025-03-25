import customtkinter as ctk
import pymysql
import datetime

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

class AccountantDashboard(ctk.CTk):
    def __init__(self, cart=None):
        super().__init__()
        self.title("Окно бухгалтера")
        self.geometry("600x400")
        self.center_window(600, 400)

        # Корзина товаров для закупки
        self.cart = cart if cart is not None else []  # Корзина товаров для закупки

        self.purchase_goods_btn = ctk.CTkButton(self, text="Закупка товара", command=self.purchase_goods)
        self.purchase_goods_btn.pack(pady=5)

        self.sell_goods_btn = ctk.CTkButton(self, text="Продажа товара", command=self.sell_goods)
        self.sell_goods_btn.pack(pady=5)

        self.financial_report_btn = ctk.CTkButton(self, text="Финансовый отчет", command=self.financial_report)
        self.financial_report_btn.pack(pady=5)

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
        # Закрытие текущего окна, если оно открыто
        if self.winfo_exists():
            self.destroy()

        # Открытие окна логина
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

        # Получаем список товаров из базы данных
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        products = cursor.fetchall()
        conn.close()

        if not products:
            print("Ошибка: в базе данных нет товаров!")
            return

        self.product_dict = {f"{p[1]} (Цена: {p[2]})": {"id": p[0], "name": p[1], "price": p[2]} for p in products}

        self.selected_product = ctk.StringVar(value=list(self.product_dict.keys())[0])  # По умолчанию первый товар

        # ✅ Обновляем выбранный товар при смене в ComboBox
        def update_selected_product(choice):
            self.selected_product.set(choice)

        product_dropdown = ctk.CTkComboBox(
            purchase_window, values=list(self.product_dict.keys()), variable=self.selected_product,
            command=update_selected_product  # Обновляем переменную при выборе
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

            # Создаем запись о поставке в таблице purchases
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            # Записываем новую поставку
            cursor.execute("INSERT INTO purchases (purchase_date) VALUES (NOW())")
            purchase_id = cursor.lastrowid  # Получаем ID последней вставленной записи

            # Записываем товары с привязкой к поставке
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
            self.cart.clear()  # Очищаем корзину после успешной закупки
            print("Закупка успешно проведена! Ожидает подтверждения кладовщика.")

        ctk.CTkButton(purchase_window, text="Закупить", command=purchase).pack(pady=5)

    def sell_goods(self):
        pass

    def financial_report(self):
        pass


if __name__ == "__main__":
    # При старте приложения корзина может быть передана
    app = AccountantDashboard()  # Создаём окно с корзиной
    app.mainloop()
