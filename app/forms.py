from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, InputRequired
from app.models import User

CATEGORIES = [('', 'Select a category'), ('ironing', 'Ironing'), ('driving', 'Driving'),
              ('ticket', 'Tickets'), ('survey', 'Survey')]
SERVICE_TYPES = [('', 'Select a choice'), ('sup', 'I want to supply a service'),
                 ('dem', 'I need a service fulfilled')]
POSSIBLE_INSTUTIONS = ['Carnegie Mellon University', 'New York University',
                       'Princeton University', 'Rutgers University',
                       'University of Alabama', 'University of Michigan']
INSTITUTIONS = [('', 'Select an institution')] + [(inst, inst) for inst in POSSIBLE_INSTUTIONS]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    institution = SelectField('Institution', validators=[InputRequired()],
                              choices=INSTITUTIONS, default='')
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
    username = StringField('Username', validators=[InputRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    demand = SelectField('What do you want to do?', choices = SERVICE_TYPES, 
                         validators=[InputRequired()], default='')
    category = SelectField('Service category', choices = CATEGORIES, 
                           validators=[InputRequired()], default='')
    price = FloatField('Compensation for service ($)', validators=[InputRequired()])
    title = StringField('Listing title', validators=[InputRequired(), Length(max=140)])
    post = TextAreaField('Additional listing info', validators=[InputRequired(), Length(max=500)])
    submit = SubmitField('Submit')
