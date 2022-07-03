
from flask_security import UserMixin, RoleMixin
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from flask_app_init import db
import enum

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


# class Airport(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(4))
#     # invoices = db.relationship('Invoice', backref='airport', lazy=True)
#
#     def __repr__(self):
#         return self.name


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
    number = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(1024))
    weight = db.Column(db.String(1024))
    place = db.Column(db.String(1024))
    status = db.Column(db.Integer(), default=0)
    sender = db.Column(db.String(1024))
    recipient = db.Column(db.String(1024))

    # airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)


