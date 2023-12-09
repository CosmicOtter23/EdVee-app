from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from edvee.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
      if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
          raise ValidationError('Email taken')


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = TextAreaField('Description')
   #  los = TextAreaField('Learning Outcomes')
   #  content = TextAreaField('Content')
   #  las = TextAreaField('Learning Activities')
   #  assessments = TextAreaField('Assessments')
    submit = SubmitField('Post')


class ElementForm(FlaskForm):
    los = TextAreaField('Learning Outcomes')
    losDesc = TextAreaField('Learning Outcomes Description')
    content = TextAreaField('Content')
    losDesc = TextAreaField('Content Description')
    las = TextAreaField('Learning Activities')
    losDesc = TextAreaField('Learning Activities Description')
    assessments = TextAreaField('Assessments')
    losDesc = TextAreaField('Assessments Description')
    submit = SubmitField('Post')


class ElementForm2(FlaskForm):
    name = StringField('Name')
    desc = TextAreaField('Description')
    id = IntegerField('ID')
    elementNo = HiddenField('Element No')
    submit = SubmitField('Submit')
