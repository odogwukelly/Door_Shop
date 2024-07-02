from shop import app, db
from flask import render_template, url_for, redirect, flash, session, request
from shop.customer.models import Customer, Order, OrderItem, Product, Category
from shop.customer.form import UpdateProfileForm
from shop.admin.form import AddProductForm, CategoryForm, EditCategoryForm, EditProductForm, UpdateOrderStatusForm
from flask_login import login_required, current_user
import os, re, json









@app.route("/all-order", methods=['GET', 'POST'])
@login_required
def allOrder_page():
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    orders = Order.query.all()
    total_orders = Order.query.count()

    cart = session.get('cart', {})
    form = UpdateOrderStatusForm()
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('admin/allOrder.html', orders=orders, total_orders=total_orders, total_price=total_price, form=form)



@app.route("/order/<int:order_id>/update", methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('landing_page'))
    
    order = Order.query.get_or_404(order_id)
    form = UpdateOrderStatusForm()
    
    if form.validate_on_submit():
        order.status = form.status.data
        db.session.commit()
        flash('Order status has been updated!', 'success')
        return redirect(url_for('allOrder_page'))
    elif request.method == 'GET':
        form.status.data = order.status
    
    return render_template('admin/edit_order.html', form=form, order=order)






# Utility function to save images
def save_image(image_data):
    import secrets
    from PIL import Image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_data.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/product_images', image_fn)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Resize the image if necessary
    output_size = (300, 300)
    i = Image.open(image_data)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


def delete_image(image_filename):
    if image_filename:  # Check if the image filename is not None or empty
        image_path = os.path.join(app.root_path, 'static/product_images', image_filename)
        
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                return True
            else:
                return False  # File doesn't exist
        except Exception as e:
            print(f"Error deleting image file {image_filename}: {e}")
            return False  # Error occurred during deletion
    return False  # No image filename provided


@app.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    category = Category.query.get_or_404(category_id)
    
    # Check if any products are associated with this category
    products = Product.query.filter_by(category_id=category_id).all()
    
    if products:
        for product in products:
            # Delete associated product images
            delete_image(product.image_1)
            delete_image(product.image_2)
            delete_image(product.image_3)
            db.session.delete(product)
    
    db.session.delete(category)
    db.session.commit()
    flash('Category and associated products deleted successfully!', 'success')
    return redirect(url_for('addCategory_page'))


@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    product = Product.query.get_or_404(product_id)
    
    # Delete associated product images
    delete_image(product.image_1)
    delete_image(product.image_2)
    delete_image(product.image_3)
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('allProduct_page'))


@app.route('/category/<int:category_id>')
@login_required
def view_products_by_category(category_id):
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('customer/index.html', category=category, products=products)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard_page():
    completed_orders = Order.query.filter_by(status='Completed').all()

    # Calculate the total cost
    total_cost = sum(
        item.product.price * item.quantity
        for order in completed_orders
        for item in order.order_items
    )


    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    customers = Customer.query.all()
    total_customers = Customer.query.count()
    orders = Order.query.all()
    total_orders = Order.query.count()
    return render_template('admin/dashboard.html', total_cost=total_cost, total_orders=total_orders, customers=customers, total_customers=total_customers, orders=orders)


@app.route("/all-product", methods=['GET', 'POST'])
@login_required
def allProduct_page():
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    products = Product.query.all()
    total_products = Product.query.count()
    return render_template('admin/allProduct.html', products=products, total_products=total_products)



@app.route("/all-customers", methods=['GET', 'POST'])
@login_required
def allCustomer_page():
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    customers = Customer.query.all()
    total_customer = Customer.query.count()
    return render_template('admin/all_customer.html', customers=customers, total_customer=total_customer)








@app.route("/add-product", methods=['GET', 'POST'])
@login_required
def addProduct_page():
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('landing_page'))
    form = AddProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    if form.validate_on_submit():
        # Split the size and color fields into lists and then convert them to JSON strings
        sizes = re.split(r'[,\s]+', form.size.data.strip())
        colors = re.split(r'[,\s]+', form.color.data.strip())
        product = Product(
            title=form.title.data,
            price=form.price.data,
            description=form.description.data,
            size=json.dumps(sizes),  # Store as JSON string
            color=json.dumps(colors),  # Store as JSON string
            quantity=form.quantity.data,
            category_id=form.category.data,
            featured_product=form.featured_product.data
        )
        if form.image_1.data:
            product.image_1 = save_image(form.image_1.data)
        if form.image_2.data:
            product.image_2 = save_image(form.image_2.data)
        if form.image_3.data:
            product.image_3 = save_image(form.image_3.data)
        db.session.add(product)
        db.session.commit()
        flash('Product has been added!', 'success')
        return redirect(url_for('addProduct_page'))
    return render_template('admin/addProduct.html', form=form)





@app.route("/edit_category/<int:category_id>", methods=['GET', 'POST'])
@login_required
def editCategory_page(category_id):
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('landing_page'))
    category = Category.query.get_or_404(category_id)
    form = EditCategoryForm(obj=category)  # Initialize form with current category data
    
    if form.validate_on_submit():
        new_name = form.name.data.strip()
        if new_name == category.name:
            flash("No changes were made", 'info')
        else:
            category.name = new_name
            try:
                db.session.commit()
                flash('Category updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating category: {str(e)}', 'danger')
        
        return redirect(url_for('addCategory_page'))
    
    # Pre-populate form data with current category name for GET requests or initial form display
    form.name.data = category.name
    
    categories = Category.query.all()
    return render_template('admin/editCategory.html', form=form, categories=categories, category=category)

@app.route("/edit_product/<int:product_id>", methods=['GET', 'POST'])
@login_required
def editProduct_page(product_id):
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('landing_page'))
    
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(obj=product)  # Populate form fields with existing product data

    if form.validate_on_submit():
        # Update product details
        product.title = form.title.data
        product.price = form.price.data
        product.description = form.description.data
        product.size = form.size.data
        product.color = form.color.data
        product.quantity = form.quantity.data
        product.category_id = form.category.data

        # Handle image uploads
        if 'image_1' in request.files:
            image_1_file = request.files['image_1']
            if image_1_file.filename:
                if product.image_1:
                    delete_image(product.image_1)  # Delete existing image
                product.image_1 = save_image(image_1_file)

        if 'image_2' in request.files:
            image_2_file = request.files['image_2']
            if image_2_file.filename:
                if product.image_2:
                    delete_image(product.image_2)  # Delete existing image
                product.image_2 = save_image(image_2_file)

        if 'image_3' in request.files:
            image_3_file = request.files['image_3']
            if image_3_file.filename:
                if product.image_3:
                    delete_image(product.image_3)  # Delete existing image
                product.image_3 = save_image(image_3_file)

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('allProduct_page'))

    # If GET request, populate form fields with current product data
    return render_template('admin/editProduct.html', form=form, product=product)

@app.route("/add-category", methods=['GET', 'POST'])
@login_required
def addCategory_page():
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category has been added!', 'success')
        return redirect(url_for('addCategory_page'))
    categories = Category.query.all()
    total_categories = Category.query.count()
    return render_template('admin/addCategory.html', form=form, categories=categories, total_categories=total_categories)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def setting_page():
    if current_user.is_authenticated and not current_user.is_admin:
            return redirect(url_for('landing_page'))
    form = UpdateProfileForm()
    return render_template('admin/setting.html', form=form)


