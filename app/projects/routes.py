from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.projects import bp
from app.models import User, Project
from importlib import import_module

@bp.route("/", methods=['GET', 'POST'])
@login_required
def projects():
    # (WIP) Pagination
    projects = [Project(**project) for project in User.get_projects(current_user.id)]
    return render_template("projects/projects.html", title="Projects", projects=projects)

@bp.route("/<projectname>", methods=['GET', 'POST'])
@login_required
def project(projectname):
    project = Project.get_project(projectname=projectname)
    module_name = "app.projects."+project.projectname
    proj_handler = import_module(module_name).__getattribute__("handler")()
    return render_template("projects/project.html", title=f"{project.projectname}", project=project, proj_handler=proj_handler)