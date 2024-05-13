from application.database import db
from flask_sqlalchemy import SQLAlchemy



# Association table for users and products
user_task = db.Table('user_task',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('task_id', db.Integer, db.ForeignKey('task.task_id')))


# Product model
class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(1000))
   

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', secondary=user_task,
                               backref=db.backref('users', lazy='dynamic'))
