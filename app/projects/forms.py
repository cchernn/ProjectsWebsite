from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Regexp
from app.models import Project

class CreateProjectForm(FlaskForm):
    projectname = StringField("Project Name", validators=[DataRequired(), Regexp(r'^[\w@#&+-]+$')])
    description = TextAreaField("Description", validators=[Length(min=0, max=140)])
    submit = SubmitField("Create Project")

    def validate_projectname(self, projectname):
        project = Project.get_project(projectname=self.projectname.data)
        if project is not None:
            raise ValidationError("Please use a different project name.")

class RequestProjectAccessForm(FlaskForm):
    submit = SubmitField("Request Access")