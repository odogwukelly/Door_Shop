from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, FileField, PasswordField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed
from shop.customer.models import Category




class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Category')

class AddProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Length(max=600)])
    size = StringField('Size', validators=[Length(max=100)])
    color = StringField('Color', validators=[Length(max=100)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    image_1 = FileField('Image 1', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    image_2 = FileField('Image 2', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    image_3 = FileField('Image 3', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Product')


class EditCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Update Category')

class EditProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image_1 = FileField('Image 1')
    image_2 = FileField('Image 2')
    image_3 = FileField('Image 3')
    category = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Product')

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]


class UpdateOrderStatusForm(FlaskForm):
    status = SelectField( '', choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Update  Order Status')