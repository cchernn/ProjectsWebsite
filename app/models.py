from datetime import datetime
from time import time
from flask_login import UserMixin, current_user
import boto3
from boto3.dynamodb.conditions import Key
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask import current_app, url_for, redirect, flash
import jwt
from hashlib import md5
from uuid import uuid4
from functools import wraps

# (WIP) Better ORM

@login.user_loader
def load_user(user_id):
    return User.get_user(id=str(user_id))

def project_permission(projectid):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            project = current_user.get_project(projectid)
            if len(project) <= 0:
                flash("You do not have permissions to access this project. Please request for authorization under the Projects page.")
                return redirect(url_for("projects.projects"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class DynamoModel(object):
    def __init__(self, **kwargs):
        for key,value in kwargs.items():
            self.__setattr__(key, value)
        if "id" not in kwargs.keys():
            self.__setattr__("id", str(uuid4()))

class User(UserMixin, DynamoModel):
    userTable = current_app.extensions["dynamo"].get_table(table_name="users")
    projectTable = current_app.extensions['dynamo'].get_table(table_name="projects")

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def get_user(cls, id=None, username=None, email=None):
        items = []
        if id is not None:
            items = cls.userTable.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        elif username is not None:
            items = cls.userTable.query(IndexName="user_username", KeyConditionExpression=Key("username").eq(username))["Items"]
        elif email is not None:
            items = cls.userTable.query(IndexName="user_email", KeyConditionExpression=Key("email").eq(email))["Items"]
        if items != []:
            return cls(**items[0])
        else:
            return None

    def commit(self, new=False):
        dbinput = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "last_activity": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        if new:
            dbinput["date_created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.userTable.put_item(Item=dbinput)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                "reset_password": self.id,
                "exp": time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.get_user(id=str(id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    @classmethod
    def get_projects(cls, user_id):
        return cls.projectTable.query(IndexName="mapping_project_user", KeyConditionExpression=Key("user_id").eq(user_id))["Items"]

    def get_project(self, id):
        return self.projectTable.query(IndexName="mapping_project_user", KeyConditionExpression=Key("user_id").eq(self.id) & Key("id").eq(id))["Items"]


class Project(DynamoModel):
    projectTable = current_app.extensions['dynamo'].get_table(table_name="projects")

    def __repr__(self):
        return f"<Project {self.projectname}>"

    @classmethod
    def get_project(cls, id=None, projectname=None):
        items = []
        if id is not None:
            items = cls.projectTable.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        elif projectname is not None:
            items = cls.projectTable.query(IndexName="project_projectname", KeyConditionExpression=Key("projectname").eq(projectname))["Items"]
        if items != []:
            return cls(**items[0])
        else:
            return None

    @classmethod
    def get_projects(cls, id=None):
        items = cls.projectTable.scan()["Items"]
        public_projs = [x for x in items if x["user_id"] == "PUBLIC"]
        private_projs = [x for x in items if x["user_id"] != "PUBLIC"]
        unique_pub_projs = list({x["id"]:x for x in public_projs}.values())
        unique_pvt_projs = list({x["id"]:x for x in private_projs}.values())
        projects = {}
        projects["public"] = [cls(**project) for project in unique_pub_projs]
        if id:
            owned_projs = [x for x in private_projs if x['user_id'] == id]
            owned_projs_ids = [x["id"] for x in owned_projs]
            projects["auth"] = [cls(**project) for project in owned_projs]
            unowned_projs = []
            for proj in unique_pvt_projs:
                if proj["id"] not in owned_projs_ids:
                    unowned_projs.append(proj)
            if len(unowned_projs) > 0: projects["private"] = [cls(**project) for project in unowned_projs]
        return projects

    def commit(self, user_id):
        dbinput = {
            "id": self.id,
            "projectname": self.projectname,
            "user_id": user_id,
            "date_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "date_created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        if self.description:
            dbinput["description"] = self.description
        self.projectTable.put_item(Item=dbinput)