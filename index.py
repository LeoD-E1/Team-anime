from flask import Flask, render_template, request, jsonify, Response, redirect
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from templates import db_format, forms
import database
from bson import json_util
from bson.objectid import ObjectId
import json


app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "x\x02\x02\xc7\xbdAS\xd3\x02\xac{\xec\xa5\xffA\xb1g\xe57k\x80\x0c\x80\xc7\xf4K\x8b\xbe\xf4\x08\x98\xf9"
bcrypt = Bcrypt(app)

@app.route("/", methods=["GET"])
def home():
    cards = database.mongo.db.anime.find()    
    return render_template("home.html", cards=cards)

@app.route("/video", methods=["GET"])
def video():

    cards = database.mongo.db.anime.find()
    return render_template("video.html", cards=cards)

@app.route("/animes", methods=["GET"])
def get_animes():
    anime = database.mongo.db.anime.find()
    response = json_util.dumps(anime)
    return Response(response, mimetype="application/json")


@app.route("/anime/<id>", methods=["GET"])
def get_anime(id):
    anime = database.mongo.db.anime.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(anime)
    return Response(response, mimetype="application/json")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    form = forms.Signup()

    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        loged_user = database.mongo.db.users.find_one({"username": username})
        loged_email = database.mongo.db.users.find_one({"email": email})

        if loged_user:
            return "El nombre de usuario elegido ya esta en uso."
        elif loged_email:
            return "Ya se registro una cuenta de TeamAnime asociada a este mail"
        else:
            id = database.mongo.db.users.insert(
                {"username": username, "email": email, "password": hashed_password}
            )
            return "Registrado con exito."

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = forms.Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        find_user = database.mongo.db.users.find_one({"username": username})

        if find_user:
            print(find_user["password"], find_user["username"])
            hashed_password = bcrypt.generate_password_hash(password)
            checked_password = bcrypt.check_password_hash(
                find_user["password"], hashed_password
            )

            if checked_password:
                print("usuario correcto")
            else:
                print("contraseña incorrecta")
        else:
            print("usuario inexistente")

    return render_template("login.html", form=form)


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({"message": "Resource not found: " + request.url, "status": 404})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)

