import customtkinter as ctk
import pymysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"


class AccountantDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Окно бухгалтера")
        self.geometry("600x400")

        self.cart = []

        self.purchase_goods_btn = ctk.CTkButton(self, text="Закупка товара", command=self.purchase_goods)
        self.purchase_goods_btn.pack(pady=5)

        self.sell_goods_btn = ctk.CTkButton(self, text="Продажа товара", command=self.sell_goods)
        self.sell_goods_btn.pack(pady=5)

        self.financial_report_btn = ctk.CTkButton(self, text="Финансовый отчет", command=self.financial_report)
        self.financial_report_btn.pack(pady=5)

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

        self.product_dict = {f"{p[1]} (Цена: {p[2]})": {"id": p[0], "name": p[1], "price": p[2]} for p in products}

        self.selected_product = ctk.StringVar()
        product_dropdown = ctk.CTkComboBox(purchase_window, values=list(self.product_dict.keys()),
                                           variable=self.selected_product)
        product_dropdown.pack(pady=5)

        ctk.CTkLabel(purchase_window, text="Количество:").pack()
        entry_quantity = ctk.CTkEntry(purchase_window)
        entry_quantity.pack()

        cart_listbox = ctk.CTkTextbox(purchase_window, height=100)
        cart_listbox.pack()

        def add_to_cart():
            selected = self.selected_product.get()
            quantity = entry_quantity.get()
            if selected and quantity.isdigit():
                product_data = self.product_dict[selected]
                self.cart.append({"id": product_data["id"], "name": product_data["name"],
                                  "price": product_data["price"], "quantity": int(quantity)})
                cart_listbox.insert("end", f"{product_data['name']} - {quantity} шт.\n")
                print(f"Товар добавлен в корзину: {product_data['name']} - {quantity} шт.")

        ctk.CTkButton(purchase_window, text="Добавить в корзину", command=add_to_cart).pack(pady=5)

        def purchase():
            if not self.cart:
                print("Корзина пуста, невозможно выполнить закупку!")
                return

            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()

            for item in self.cart:
                product_id = item["id"]
                quantity = item["quantity"]
                total_price = item["quantity"] * item["price"]

                cursor.execute(
                    "INSERT INTO transactions (transaction_type, product_id, quantity, total_price, status) VALUES ('purchase', %s, %s, %s, 'pending')",
                    (product_id, quantity, total_price))

            conn.commit()
            conn.close()
            self.cart.clear()
            print("Закупка успешно проведена! Ожидает подтверждения кладовщика.")

        ctk.CTkButton(purchase_window, text="Закупить", command=purchase).pack(pady=5)

    def sell_goods(self):

        pass

    def financial_report(self):

        pass


if __name__ == "__main__":
    app = AccountantDashboard()
    app.mainloop()
