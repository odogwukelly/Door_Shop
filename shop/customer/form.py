# Import necessary modules and classes
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from shop.customer.models import Customer


# Define the registration form for user sign-up
class RegistrationForm(FlaskForm):
    # Define form fields and associated validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Select', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')])
    profile_img = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        customer = Customer.query.filter_by(username=username.data).first()
        if customer:
            raise ValidationError('Username already Exit')
        
    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('Email already Exit')


# Define the login form for user authentication
class LoginForm(FlaskForm):
    # Define form fields for email and password
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
        
    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if not customer:
            raise ValidationError("User not found")


# Define the update form for user 
class UpdateProfileForm(FlaskForm):
    # Define form fields and associated validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Select', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')])
    profile_img = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            customer = Customer.query.filter_by(username=username.data).first()
            if customer:
                raise ValidationError("You can't perform this action")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError("You can't perform this action")
            

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Place Order')