from datetime import datetime
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    phone = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    orders = db.relationship("Order", back_populates="user", lazy=True)
    addresses = db.relationship("Address", back_populates="user", cascade="all, delete-orphan")
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    promo_text = db.Column(db.String(255))
    category = db.Column(db.String(80), nullable=False, index=True)
    address = db.Column(db.String(255), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), default=Decimal("2.99"), nullable=False)
    minimum_order = db.Column(db.Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    delivery_time_min = db.Column(db.Integer, default=30, nullable=False)
    rating = db.Column(db.Numeric(2, 1), default=Decimal("4.0"), nullable=False)
    is_open = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    products = db.relationship("Product", back_populates="restaurant", cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship("Review", back_populates="restaurant", cascade="all, delete-orphan", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    stock = db.Column(db.Integer, default=100, nullable=False)
    calories = db.Column(db.Integer)
    is_vegetarian = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    restaurant = db.relationship("Restaurant", back_populates="products")
    order_items = db.relationship("OrderItem", back_populates="product", lazy=True)


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_percent = db.Column(db.Numeric(5, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    max_discount = db.Column(db.Numeric(10, 2))
    active = db.Column(db.Boolean, default=True, nullable=False)
    expires_at = db.Column(db.DateTime)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    is_default = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", back_populates="addresses")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(30), default="pending", nullable=False)
    payment_method = db.Column(db.String(30))
    payment_reference = db.Column(db.String(80))
    cash_received = db.Column(db.Numeric(10, 2))
    change_due = db.Column(db.Numeric(10, 2))
    customer_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="orders")
    restaurant = db.relationship("Restaurant")
    address = db.relationship("Address")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (db.UniqueConstraint("user_id", "restaurant_id", name="uq_user_restaurant_favorite"),)

    user = db.relationship("User", back_populates="favorites")
    restaurant = db.relationship("Restaurant")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="reviews")
    restaurant = db.relationship("Restaurant", back_populates="reviews")
