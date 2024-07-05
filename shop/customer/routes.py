from shop import app, bcrypt, db
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, session, abort
from .form import RegistrationForm, LoginForm, UpdateProfileForm, CheckoutForm
from .models import Customer, Order, OrderItem
from .models import Product, Category
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os, stripe, json
from dotenv import load_dotenv
load_dotenv()




stripe.api_key = 'sk_test_51OPmzIDIrzfDF0fX1t8Dgg47h0OgCdgf6t9IouUZqRLCj81hZ1to1SKPo9KW43nOrNkA2UjGlB3EinymXei7cn4e00yhLq6lKb'


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')

    form = CheckoutForm()
    cart = session.get('cart', {})
    
    # Check if the cart is empty and redirect if it is
    if not cart:
        flash('Your cart is empty. Please add items to your cart before checking out.', 'warning')
        return redirect(url_for('cart'))

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        stripe_token = request.form.get('stripeToken')

        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),  # amount in cents
                currency='usd',
                description='Payment for order',
                source=stripe_token,
                metadata={'order_id': '6735'}
            )

            # Save order to the database
            order = Order(user_id=current_user.id)
            db.session.add(order)
            db.session.commit()
            print(f"Created Order: {order}")

            for item in cart.values():
                if 'id' not in item:
                    current_app.logger.error('Item missing ID: %s', json.dumps(item, indent=2))
                    continue  # Skip this item or handle the error as needed
                selected_color = request.form.get('selected_color')
                selected_size = request.form.get('selected_size')
                order_item = OrderItem(
                    order_id=order.id, 
                    product_id=item['id'], 
                    quantity=item['quantity'],
                    selected_color=item['selected_color'],
                    selected_size=item['selected_size'])
                db.session.add(order_item)
                print(f"Created OrderItem: {order_item}")
            db.session.commit()

            session.pop('cart', None)
            flash('Your payment was successful!', 'success')
            return redirect(url_for('order_confirmation', order_id=order.id))
        except stripe.error.StripeError as e:
            flash(f'Error processing payment: {e}', 'danger')
            return redirect(url_for('checkout'))

    return render_template('customer/checkout.html', image_file=image_file, form=form, cart=cart, total_price=total_price)











@app.route('/order_confirmation/<int:order_id>', methods=['POST', 'GET'])
@login_required
def order_confirmation(order_id):
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')

    order = Order.query.get_or_404(order_id)
    user = Customer.query.get_or_404(order.user_id)
    print(order)
    
    # Retrieve order items explicitly
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    print(f"Order Items: {order_items}")

    total_price = sum(item.product.price * item.quantity for item in order_items)
    print(total_price)

    return render_template('customer/order_confirmation.html', user=user, image_file=image_file, order=order, order_items=order_items, total_price=total_price)









@app.route("/my_orders", methods=['POST'])
@login_required
def my_orders():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')

    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('customer/my_order.html', orders=orders, image_file=image_file)










@app.context_processor
def cart_counter():
    def count_items_in_cart():
        if 'cart' not in session:
            return 0
        cart = session['cart']
        # Count each unique product only once
        total_items = len(cart)
        return total_items
    return dict(cart_counter=count_items_in_cart)


@app.route("/cart")
def cart():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')


    if 'cart' not in session:
        session['cart'] = {}
        
    
    cart = session['cart']
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return render_template('customer/cart.html', cart=cart, total_price=total_price, image_file=image_file)


@app.route("/add_to_cart/<int:product_id>", methods=['POST'])
def add_to_cart(product_id):
    cart_product = Product.query.get_or_404(product_id)

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        sizes = cart_product.size.replace(' ', '').replace('[', '').replace(']', '').replace('"', '').split(',')
        colors = cart_product.color.replace(' ', '').replace('[', '').replace(']', '').replace('"', '').split(',')

        cart[str(product_id)] = {
            'id' : product_id,
            'title': cart_product.title,
            'price': cart_product.price,
            'quantity': 1,
            'image': cart_product.image_1,
            'sizes': sizes,
            'colors': colors,
            'selected_size': sizes[0] if sizes else '',
            'selected_color': colors[0] if colors else ''
        }

    session['cart'] = cart
    flash(f'Added {cart_product.title} to your cart', 'success')
    return redirect(url_for('landing_page', product_id=product_id))


# def add_to_cart(product_id):
#     product = Product.query.get(product_id)
#     if product:
#         cart = session.get('cart', {})
#         if product_id not in cart:
#             cart[product_id] = {
#                 'id': product.id,
#                 'title': product.title,
#                 'price': product.price,
#                 'quantity': 1,
#                 'image': product.image_1,
#                 'color': product.color,
#                 'size': product.size
#             }
#         else:
#             cart[product_id]['quantity'] += 1
#         session['cart'] = cart




@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
@login_required
def update_cart_quantity(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = int(request.form['quantity'])
        cart[str(product_id)]['selected_size'] = request.form['size']
        cart[str(product_id)]['selected_color'] = request.form['color']
        session['cart'] = cart
        flash('Cart updated successfully', 'success')
    else:
        flash('Product not found in cart', 'danger')
    return redirect(url_for('cart'))


@app.route("/remove_from_cart/<int:product_id>", methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

















def save_pics(form_pics):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pics.filename)
    path_ext = 'customer/assets/profile_pics/'
    pics_fn = random_hex + f_ext
    pics_path = os.path.join(current_app.root_path, 'static', path_ext, pics_fn)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(pics_path), exist_ok=True)
    form_pics.save(pics_path)
    return pics_fn

def delete_image(image_filename):
    if image_filename:  # Check if the image filename is not None or empty
        image_path = os.path.join(app.root_path, 'static/customer/assets/profile_pics/', image_filename)
        
        if os.path.exists(image_path):
            os.remove(image_path)
            return True
    return False



@app.route("/")
def landing_page():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='customer/assets/profile_pics/defaults.png')

    featured_products = Product.query.filter_by(featured_product=True).all()
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("customer/index.html", image_file=image_file, products=products,  f_product={'featured_product': featured_products}, categories=categories )


@app.route("/about")
def about_page():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')
    return render_template("customer/about.html", image_file=image_file)


@app.route("/contact")
def contact_page():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')
    return render_template("customer/contact.html", image_file=image_file)


@app.route('/products/')
def product_page():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')
    
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("customer/products.html", image_file=image_file, categories=categories, products=products)

@app.route('/get_products', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id')
    if category_id:
        products = Product.query.filter_by(category_id=category_id).all()
    else:
        products = Product.query.all()
    
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'description': product.description,
            'size': product.size,
            'color': product.color,
            'quantity': product.quantity,
            'image_1': product.image_1,
            'image_2': product.image_2,
            'image_3': product.image_3,
        })

    return jsonify({'products': products_list})




@app.route("/product/<int:product_id>", methods=['POST', 'GET'])
def productDetails_page(product_id):
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(category_id=product.category_id).filter(Product.id != product_id).limit(4).all()
    return render_template("customer/product_detail.html", product=product, image_file=image_file, related_products=related_products)


@app.route("/cart")
def cart_page():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')
    return render_template("customer/cart.html", image_file=image_file)


@app.route('/signup', methods=['GET', 'POST'])
def signUp_page():
    if current_user.is_authenticated:
        return redirect(url_for('landing_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        if form.profile_img.data:
            pics_file = save_pics(form.profile_img.data)
        else:
            pics_file = None  # or set a default image path if you prefer
        
        customer = Customer(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            image_file=pics_file
        )
        
        db.session.add(customer)
        db.session.commit()
        
        flash("Account created successfully!", "success")
        return redirect(url_for('login_page'))
    
    return render_template("customer/signUp.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('landing_page'))

    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()

        if customer:
            check_password = bcrypt.check_password_hash(customer.password, form.password.data)
            if check_password:
                login_user(customer, remember=form.remember.data)
                next_page = request.args.get('next')

                if next_page:
                    return redirect(next_page)
                else:
                    if customer.is_admin:  # Assuming there's an `is_admin` attribute in the Customer model
                        flash(f'Admin Logged In Successfully', 'success')
                        return redirect(url_for('landing_page'))  # Replace with your admin dashboard URL
                    else:
                        flash(f'You have successfully Logged In', 'success')
                        return redirect(url_for('landing_page'))
            else:
                flash('Invalid Password', 'danger')
        else:
            flash('No account found with that email', 'danger')

    return render_template("customer/login.html", form=form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful", 'success')
    return redirect(url_for('landing_page'))



@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        if form.profile_img.data:
            # Delete old profile image if exists
            delete_image(current_user.image_file)

            # Save new profile image
            pics_file = save_pics(form.profile_img.data)
            current_user.image_file = pics_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data
        current_user.date_of_birth = form.date_of_birth.data

        db.session.commit()
        flash("Profile updated successfully!", 'success')
        return redirect(url_for('profile_page'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.date_of_birth.data = current_user.date_of_birth

    if current_user.is_authenticated:
        image_file = url_for('static', filename='customer/assets/profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='admin/assets/profile_pics/defaults.png')

    return render_template('customer/profile.html', image_file=image_file, form=form)






    