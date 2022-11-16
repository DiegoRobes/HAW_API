import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.secret_key = os.environ.get('SERVER_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///HAW.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    author = db.Column(db.String(100), unique=False, nullable=True)
    work = db.Column(db.String(300), unique=False, nullable=True)
    publisher = db.Column(db.String(200), unique=False, nullable=True)


class Novella(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    author = db.Column(db.String(100), unique=False, nullable=True)
    work = db.Column(db.String(300), unique=False, nullable=True)
    publisher = db.Column(db.String(200), unique=False, nullable=True)


class Novelette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    author = db.Column(db.String(100), unique=False, nullable=True)
    work = db.Column(db.String(300), unique=False, nullable=True)
    publisher = db.Column(db.String(200), unique=False, nullable=True)


class ShortStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    author = db.Column(db.String(100), unique=False, nullable=True)
    work = db.Column(db.String(300), unique=False, nullable=True)
    publisher = db.Column(db.String(200), unique=False, nullable=True)


with app.app_context():
    db.create_all()

    with open("raw_csv/HAW(Novel).csv") as file:
        reader = csv.reader(file)
        novels = [i for i in reader if i]

        for i in novels:
            entry = Novel(
                year=i[0],
                author=i[1],
                work=i[2],
                publisher=i[3]
            )
            db.session.add(entry)
            db.session.commit()

    with open("raw_csv/HAW(NOVELLA).csv") as file:
        reader = csv.reader(file)
        novellas = [i for i in reader if i]

        for i in novellas:
            try:
                entry = Novella(
                    year=i[0],
                    author=i[1],
                    work=i[2],
                    publisher=i[3]
                )
                db.session.add(entry)
                db.session.commit()
            except IndexError:
                entry = Novella(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                db.session.add(entry)
                db.session.commit()

    with open("raw_csv/HAW(NOVELETTE).csv") as file:
        reader = csv.reader(file)
        novelettes = [i for i in reader if i]

        for i in novelettes:
            try:
                entry = Novelette(
                    year=i[0],
                    author=i[1],
                    work=i[2],
                    publisher=i[3]
                )
                db.session.add(entry)
                db.session.commit()
            except IndexError:
                entry = Novelette(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                db.session.add(entry)
                db.session.commit()

    with open("raw_csv/HAW(SHORT STORY).csv") as file:
        reader = csv.reader(file)
        s_s = [i for i in reader if i]
        for i in s_s:
            try:
                entry = ShortStory(
                    year=i[0],
                    author=i[1],
                    work=i[2],
                    publisher=i[3]
                )
                db.session.add(entry)
                db.session.commit()
            except IndexError:
                entry = ShortStory(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                db.session.add(entry)
                db.session.commit()
