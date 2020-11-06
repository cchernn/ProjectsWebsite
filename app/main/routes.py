from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, Project
from app.main.forms import EditProfileForm
from app.projects.forms import CreateProjectForm
from werkzeug.exceptions import NotFound
from datetime import datetime

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        pass

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="Home")

@bp.route("/user/<username>", methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.get_user(username=username)
    if user is None:
        abort(404)
    projects = [Project(**project) for project in User.get_projects(user_id=current_user.id)]
    # (WIP) Temp - function is only for admin
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(projectname=form.projectname.data, description=form.description.data)
        project.commit(user_id=user.id)
        flash("Congratulations, your new project is online.")
        return redirect(url_for("main.user", username=user.username))
    return render_template("user.html", title=f"{user.username} - Profile Page", user=user, projects=projects, form=form)

@bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data if form.username.data != "" else current_user.username
        current_user.email = form.email.data if form.email.data != "" else current_user.email
        if form.username.data != "" or form.email.data != "":
            current_user.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("main.user", username=current_user.username))        
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit_profile.html", title="Edit Profile", form=form)