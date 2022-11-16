import os
from flask import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import csv
from key_generator import Password
from werkzeug.security import generate_password_hash, check_password_hash

user_pass = Password()

app = Flask(__name__)
app.secret_key = os.environ.get('SERVER_KEY')
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///HAW.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(200))


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
            if not entry.query.filter_by(work=entry.work).all():
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
                if not entry.query.filter_by(work=entry.work).all():
                    db.session.add(entry)
                    db.session.commit()

            except IndexError:
                entry = Novella(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                if not entry.query.filter_by(work=entry.work).all():
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
                if not entry.query.filter_by(work=entry.work).all():
                    db.session.add(entry)
                    db.session.commit()
            except IndexError:
                entry = Novelette(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                if not entry.query.filter_by(work=entry.work).all():
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
                if not entry.query.filter_by(work=entry.work).all():
                    db.session.add(entry)
                    db.session.commit()
            except IndexError:
                entry = ShortStory(
                    year=i[0],
                    author=None,
                    work=None,
                    publisher=None
                )
                if not entry.query.filter_by(work=entry.work).all():
                    db.session.add(entry)
                    db.session.commit()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/your-key/", methods=["POST"])
def your_key():
    if request.method == "POST":
        deliver_pass = user_pass.create_pass()
        new_user = User(
            email=request.form.get("user"),
            password=generate_password_hash(password=deliver_pass,
                                            method="pbkdf2:sha256",
                                            salt_length=8)
        )
        if not new_user.query.filter_by(email=new_user.email).all():
            db.session.add(new_user)
            db.session.commit()
            return render_template("api_key.html", password=deliver_pass)
        else:
            return jsonify(Nope={f"Identity theft is not a joke": "This email is already associated with other account."
                                                                  " Try a different one."})


@app.route("/request/<int:year>", methods=["GET"])
def get(year):
    category = request.args.get("category")
    key = request.args.get("api-key")
    all_users = User.query.all()

    tables_dict = {table.__tablename__: table for table in db.Model.__subclasses__()}

    def table_object(table_name):
        return tables_dict.get(table_name)

    try:
        table = table_object(category)
        results = table.query.filter_by(year=year).all()
        if len(results) == 0:
            return jsonify(Nope={f"Bad request": f"Please check the Year: {year}"})

        verified_user = False
        for i in all_users:
            if check_password_hash(pwhash=i.password, password=key):
                verified_user = True
    except AttributeError:
        return jsonify(Nope={f"Bad request": f"Please check the Category: {category}"})

    final_delivery = []
    for i in results:
        final_delivery.append({"Author": i.author,
                               "Work": i.work,
                               "Publisher": i.publisher})
    try:
        if verified_user:
            return jsonify(success={f"Year": f"{year}",
                                    "Category": f"{category}",
                                    "Results": final_delivery})
        else:
            return jsonify(Nope={f"Wrong Password": f"{key}"})
    except AttributeError:
        return jsonify(Nope={f"Not Registered Yet": f"{key}"})


if __name__ == '__main__':
    app.run(debug=True)
