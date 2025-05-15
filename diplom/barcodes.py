def generate_barcodes_for_batch(batch_id, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT product_id, quantity 
                FROM transactions 
                WHERE purchase_id = %s AND status = 'received'
            """, (batch_id,))
            products = cursor.fetchall()

            for product in products:
                product_id = product['product_id']
                quantity = product['quantity']

                for bottle_id in range(1, quantity + 1):
                    barcode = f"{batch_id}-{product_id}-{bottle_id}"

                    cursor.execute("""
                        INSERT INTO barcodes (product_id, bottle_id, batch_id, barcode)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE barcode=VALUES(barcode)
                    """, (product_id, bottle_id, batch_id, barcode))

    except Exception as e:
        print(f"Ошибка при генерации штрих-кодов: {e}")
        raise
