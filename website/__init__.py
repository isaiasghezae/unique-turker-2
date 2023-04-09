from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# for our web app to safely communicate with other websites
from flask_cors import CORS
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


# database models; unique ID database + worker ID database; one-to-many SQL relationship
class Uniqueid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(200), unique=True)
    workers = db.relationship("Worker", backref="uniqueid", lazy=True)


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workerid = db.Column(db.String(200))
    unique_id = db.Column(db.Integer, db.ForeignKey(
        "uniqueid.id"), nullable=False)


def create_app():
    app = Flask(__name__)
    # allow communication from anyone
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = 'new-unique-turker'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    # handling database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
