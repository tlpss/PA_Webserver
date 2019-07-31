from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from server.models import User, Feeder
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PetFeederRegistrationForm(FlaskForm):
    secret_key = StringField('Feeder Key', validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    submit = SubmitField('Add Feeder')


class FeedMomentRegistrationForm(FlaskForm):
    hour = IntegerField('hour', validators= [DataRequired()])
    minute = IntegerField('minute', validators= [DataRequired()])
    amount = IntegerField('amount', validators= [DataRequired()])
    submit = SubmitField('Add Moment')

    def validate_hour(self,hour):
        hour = hour.data
        if not (hour >= 0 and hour < 24):
            raise ValidationError('enter valid time')

    def validate_minute(self,minute):
        minute = minute.data
        if not ( minute >=0 and minute < 60):
            raise ValidationError('enter valid time')

    def validate_amount(self,amount):
        amount = amount.data
        if not ( amount > 0 and amount < 100): #arbitrary upper limit!
            raise ValidationError('enter valid amount')
