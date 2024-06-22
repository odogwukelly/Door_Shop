from shop import app, db
from shop.customer.models import Customer


with app.app_context():
    db.drop_all()
    db.create_all()
    
    user = Customer.query.all()
    print(user)





