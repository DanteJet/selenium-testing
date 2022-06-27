
def test_add_to_cart_three_products(app):
    for i in range(0,3):
        app.add_first_product_to_cart()
    count = app.get_count_product_cards_in_cart()
    print("!!!")
    print(count)
    for i in range(0, count):
        app.delete_product_from_cart()
    assert app.check_no_product_in_cart(), "Cart have some products"
