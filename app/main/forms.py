from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    submit = SubmitField("Change Details")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.get_user(username=self.username.data)
            if user is not None:
                raise ValidationError("Please use a different username.")