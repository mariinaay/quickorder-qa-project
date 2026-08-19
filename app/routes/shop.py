from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..cart import add_to_cart, update_cart, cart_items, clear_cart, remove_from_cart, cart_restaurant_ids
from ..models import Product, Restaurant, Favorite, Review
from ..extensions import db

shop_bp = Blueprint("shop", __name__)


@shop_bp.post("/cart/add/<int:product_id>")
def add(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get("quantity", 1, type=int)
    quantity = max(quantity or 1, 1)

    # INTENTIONAL QA BUGS:
    # - stock=0 is allowed into the cart;
    # - a closed restaurant can still receive orders;
    # - stock is not rechecked against the requested quantity.
    if not product.available:
        flash("Produit indisponible.", "danger")
        return redirect(request.referrer or url_for("main.index"))
    existing_restaurants = cart_restaurant_ids()
    if existing_restaurants and product.restaurant_id not in existing_restaurants:
        flash("Un panier ne peut contenir que des produits du même restaurant.", "warning")
        return redirect(request.referrer or url_for("main.index"))
    add_to_cart(product.id, quantity)
    flash(f"{product.name} ajouté au panier.", "success")
    return redirect(request.referrer or url_for("main.index"))


@shop_bp.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        for product_id, quantity in request.form.items():
            if product_id.startswith("qty_"):
                try:
                    # INTENTIONAL QA BUG: quantity is not capped by current stock.
                    update_cart(product_id.replace("qty_", ""), int(quantity))
                except ValueError:
                    flash("Quantité invalide.", "danger")
    items, subtotal = cart_items()
    delivery_fee = items[0]["product"].restaurant.delivery_fee if items else 0
    total = subtotal + delivery_fee if items else 0
    return render_template("cart.html", items=items, subtotal=subtotal, delivery_fee=delivery_fee, total=total)


@shop_bp.post("/cart/remove/<int:product_id>")
def remove(product_id):
    remove_from_cart(product_id)
    flash("Produit retiré du panier.", "info")
    return redirect(url_for("shop.cart"))


@shop_bp.post("/cart/clear")
def clear():
    clear_cart()
    flash("Panier vidé.", "info")
    return redirect(url_for("shop.cart"))


@shop_bp.post("/favorite/<int:restaurant_id>")
@login_required
def toggle_favorite(restaurant_id):
    Restaurant.query.get_or_404(restaurant_id)
    favorite = Favorite.query.filter_by(user_id=current_user.id, restaurant_id=restaurant_id).first()
    if favorite:
        db.session.delete(favorite)
        flash("Restaurant retiré des favoris.", "info")
    else:
        db.session.add(Favorite(user_id=current_user.id, restaurant_id=restaurant_id))
        flash("Restaurant ajouté aux favoris.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("main.index"))


@shop_bp.post("/restaurant/<int:restaurant_id>/review")
@login_required
def review(restaurant_id):
    Restaurant.query.get_or_404(restaurant_id)
    try:
        rating = int(request.form.get("rating", 0))
    except ValueError:
        rating = 0
    comment = request.form.get("comment", "").strip()
    if rating not in range(1, 6) or not comment:
        flash("Note et commentaire obligatoires.", "danger")
        return redirect(request.referrer or url_for("main.restaurant", restaurant_id=restaurant_id))
    # INTENTIONAL QA BUG: any logged-in user can review a restaurant without ordering it.
    db.session.add(Review(user_id=current_user.id, restaurant_id=restaurant_id, rating=rating, comment=comment))
    db.session.commit()
    flash("Merci pour votre avis !", "success")
    return redirect(url_for("main.restaurant", restaurant_id=restaurant_id))
