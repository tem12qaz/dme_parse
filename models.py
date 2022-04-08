
from flask_security import UserMixin, RoleMixin

from flask_app_init import db
import enum

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class Airport(enum.Enum):
    DME = "DME"
    VKO = "VKO"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class Invoice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String(16))
    email = db.Column(db.String(1024))
    weight = db.Column(db.String(1024))
    place = db.Column(db.String(1024))
    status = db.Column(db.Integer(), default=0)
    airport = db.Column(enum.Enum(Airport))


