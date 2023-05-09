import os
from datetime import datetime

from flask import Flask
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from .bootstrap import get_or_create_app

app = get_or_create_app()

file_path = os.path.abspath(os.getcwd()) + "/src/data/mockapi.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def db_auto_create():
    """ Automatically create SQLite db if it does not exists """

    with app.app_context():
        try:
            db.session.get(RouteModel, 1)

            # Database already exists
            return False
        except sqlalchemy.exc.OperationalError:
            db.create_all()

    # Database has been created
    return True


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(80), unique=True, nullable=False, index=True)
    type_ = db.Column(db.String(10), nullable=False, default='text')
    body = db.Column(db.Text())
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now, index=True)
    expiration_date = db.Column(
        db.DateTime, index=True)

    def __repr__(self):
        return '<Route %r>' % self.path


db_auto_create()
