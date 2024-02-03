from data import Data
from flask import Flask, render_template, url_for, request, g, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
import sqlite3
import os

DATABASE = "/db/database.db"
DEBUG = True
SECRET_KEY = "12345"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "database.db")))

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return User().fromDB(user_id, D)

def connect_db():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect

def create_db():
    print("ПОДКЛЮЧЕНИЕ")
    db = connect_db()
    with app.open_resource("database.sql", mode= "r") as script:
        db.cursor().executescript(script.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        print("БАЗА ДАННЫХ ПОЛУЧЕНА")
    return g.link_db

D = None
@app.before_request
def before_request():
    global D
    db = get_db()
    D = Data(db)
   

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

#-----------------------------------------------------------------------------------#
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if request.method == "POST":
        if "new_name" in request.form:
            D.update_name(current_user.get_id(), request.form["new_name"])
            flash("Вы сменили имя")
            return redirect(url_for('settings'))
        
        if "new_password" in request.form:
            D.update_password(current_user.get_id(), request.form["new_password"])
            flash("Вы сменили пароль")
            return redirect(url_for('settings'))
        
    return render_template("settings.html", name = current_user.get_nickname())

@app.route("/profile")
@login_required
def profile():
    print("starter drinks: ", current_user.starter_drinks)
    return render_template("profile.html", 
                           nickname = current_user.get_nickname(),
                           id = current_user.get_id(),
                           fauvorite_drink = D.get_fauvorite_drink(current_user.get_id()),
                           stats = D.get_statistic(current_user.get_id())
                           )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/create_event", methods = ["POST", "GET"])
@login_required
def create_event():
    drinks = D.get_drinks(current_user.get_id())

    if request.method == "POST":
        D.add_event(current_user.get_id(),
                    request.form["title"],
                    request.form["event_date"],
                    request.form["place"],
                    request.form["description"]) 
        flash("Вы успешно добавили событие")
        return redirect(url_for("history"))
    return render_template("create_event.html", drinks = drinks)

@app.route("/drinks", methods = ["POST", "GET"])
@login_required
def drinks():
    drinks = D.get_drinks(current_user.get_id())

    if request.method == "POST":
        D.add_drink(request.form["title"], 
                    request.form["price"],
                    request.form["alcohol"],
                    request.form["volume"],
                    current_user.get_id())
        
        flash("Вы успешно добавили напиток.")
        
        return redirect(url_for("drinks"))
    
        
    return render_template("drinks.html", drinks = drinks)

@app.route("/delete_drink/<int:drink_id>")
def delete_drink(drink_id):
    D.delete_drink(drink_id)
    flash("Напиток удален")
    return redirect(url_for('drinks'))
    

@app.route("/history")
@login_required
def history():
    events = D.get_events(current_user.get_id())
    print(events)
    return render_template("history.html", events = events)

@app.route("/event/<int:event_id>", methods = ["POST", "GET"])
@login_required
def event(event_id):
    if request.method == "POST":
        D.add_drink_in_event(current_user.get_id(), event_id, request.form["drink"], request.form["volume"], request.form["price"])
        flash("Напиток добавлен", "accept")
        return redirect(url_for('event', event_id = event_id))
    return render_template("event.html",
                            drinks = D.get_drinks(current_user.get_id()),
                            drinks_in_event = D.get_drinks_in_event(event_id),
                            volume_sum = D.get_sum_of_volume(event_id),
                            price_sum = D.get_sum_of_price(event_id),
                            description = D.get_description(event_id),
                            event_info = D.get_event_info(event_id))

@app.route("/delete_event/<int:event_id>")
def delete_event(event_id): 
    D.delete_event(event_id)
    flash("Событие удалено")
    return redirect(url_for('history'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = D.get_user_by_nickname(request.form['nickname'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = User().create(user)
            login_user(user_login)
            
            return redirect("/")
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        hash = generate_password_hash(request.form["psw"])
        D.add_user(request.form['nickname'], hash)
        flash("Успешная регистрация", "accept")
        return redirect("/login")
    return render_template("register.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True)