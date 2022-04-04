from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from restaurant_appf.models import User, Restaurant, MenuItem

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])

    submit = SubmitField('Sign Up')    

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()

        if email:

            raise ValidationError('That email is taken. Please choose another one!')

class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class NewRestaurant(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    
    def validate_name(self, name):
        
        name = Restaurant.query.filter(name=name).first()
        
        if name:
            
            raise ValidationError('That name is taken. Please choose another one!')
        
class MenuItemForm(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])     
    
    