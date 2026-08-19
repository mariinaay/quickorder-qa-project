from flask import session
from .models import Product


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def add_to_cart(product_id, quantity=1):
    cart = get_cart().copy()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + int(quantity)
    save_cart(cart)


def update_cart(product_id, quantity):
    cart = get_cart().copy()
    key = str(product_id)
    quantity = int(quantity)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(cart)


def remove_from_cart(product_id):
    cart = get_cart().copy()
    cart.pop(str(product_id), None)
    save_cart(cart)


def clear_cart():
    session.pop("cart", None)


def cart_items():
    cart = get_cart()
    items = []
    subtotal = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            line_total = product.price * quantity
            items.append({"product": product, "quantity": quantity, "line_total": line_total})
            subtotal += line_total
    return items, subtotal


def cart_restaurant_ids():
    items, _ = cart_items()
    return {item["product"].restaurant_id for item in items}
