from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, Email, ValidationError, Regexp
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[Optional(), Regexp(r'^[\w@./#&+-]+$')])
    email = StringField("Email", validators=[Optional(), Email()])
    submit = SubmitField("Change Details")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.get_user(username=username.data)
            if user is not None:
                raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.get_user(email=email.data)
            if user is not None:
                raise ValidationError("Please use a different email address")