from datetime import datetime
from shop import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON



@login_manager.user_loader
def load_customer(customer_id):
    return Customer.query.get(customer_id)

class Customer(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default= "defaults.png" )
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"Customer_{self.id}('{self.username}', '{self.is_admin}', '{self.email}', '{self.image_file}', '{self.date_of_birth}', '{self.gender}', '{self.date_created}', '{self.is_admin}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    size = db.Column(db.Text, nullable=False)  # Store sizes as JSON string
    color = db.Column(db.Text, nullable=False)  # Store colors as JSON string
    quantity = db.Column(db.Integer, nullable=False)
    image_1 = db.Column(db.String(50), nullable=True)
    image_2 = db.Column(db.String(50), nullable=True)
    image_3 = db.Column(db.String(50), nullable=True)
    featured_product = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', cascade='all, delete-orphan')



    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.description}', '{self.size}', '{self.color}', '{self.quantity}', '{self.image_1}')"

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(25), nullable=False, default='Pending')
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.timestamp}', '{self.status}', '{self.order_items}')"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.order_items)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    selected_color = db.Column(db.String(50), nullable=False)
    selected_size = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.id}', '{self.order_id}', '{self.product_id}', '{self.quantity}')"