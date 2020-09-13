from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp
from app.models import User
from app.main.forms import EditProfileForm
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

@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.get_user(username=username)
    if user is None:
        abort(404)
    return render_template("user.html", title=f"{user.username} - Profile Page", user=user)

@bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template("edit_profile.html", title="Edit Profile", form=form)