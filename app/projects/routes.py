from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.projects import bp
from app.models import User, Project

@bp.route("/", methods=['GET', 'POST'])
@login_required
def projects():
    projects = [Project(**project) for project in User.get_projects(current_user.id)]
    return render_template("projects/projects.html", title="Projects", projects=projects)