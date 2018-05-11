from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, InputRequired
from app.models import User
from . import model_constants as m_c

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    institution = SelectField('Institution', validators=[InputRequired()],
                              choices=m_c.INSTITUTIONS_FORM, default='')
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class PostForm(FlaskForm):
    demand = SelectField('What do you want to do?', choices = m_c.SERVICE_TYPES_FORM, 
                         validators=[InputRequired()], default='')
    broad_category = SelectField('Service category', choices = m_c.BROAD_CATEGORIES_FORM, 
                                 validators=[InputRequired()], default='')      
    category = SelectField('Service category', choices = m_c.SERVICES_FORM + m_c.ITEMS_FORM, 
                           validators=[InputRequired()], default='')
    price = FloatField('Compensation for service ($)', validators=[InputRequired()])
    title = StringField('Listing title', validators=[InputRequired(), Length(max=140)])
    body = TextAreaField('Additional listing info', validators=[InputRequired(), Length(max=500)])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    rating = SelectField('Rate your experience out of 5 stars', choices = m_c.RATINGS_FORM, 
                         validators=[InputRequired()], default='')
    body = TextAreaField('Let others know about your experience', validators=[InputRequired(), Length(max=500)])
    submit = SubmitField('Submit')

