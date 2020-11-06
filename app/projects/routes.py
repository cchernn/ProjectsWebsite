from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.projects import bp
from app.models import User, Project
from app.projects.forms import RequestProjectAccessForm
from importlib import import_module

@bp.route("/", methods=['GET', 'POST'])
def projects():
    # (WIP) Pagination
    if current_user.is_authenticated:
        projects = Project.get_projects(id=current_user.id)
    else:
        projects = Project.get_projects()
    form = RequestProjectAccessForm()
    return render_template("projects/projects.html", title="Projects", projects=projects, form=form)

@bp.route("/requestprojectaccess/<projectid>", methods=['POST'])
@login_required
def requestprojectaccess(projectid):
    form = RequestProjectAccessForm()
    if form.validate_on_submit():
        project = Project.get_project(id=projectid)
        project.commit(user_id=current_user.id)
        flash(f"You are now authorized to follow project {project.projectname}.")
    return redirect(url_for("projects.projects"))

## General Project Page
@bp.route("/<projectname>", methods=['GET', 'POST'])
# @login_required
def project(projectname):
    project = Project.get_project(projectname=projectname)
    module_name = "app.projects."+project.projectname
    proj_handler = import_module(module_name).__getattribute__("handler")()
    return render_template("projects/project.html", title=f"{project.projectname}", project=project, proj_handler=proj_handler)