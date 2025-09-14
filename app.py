from flask import Flask
import sqlalchemy as sa

engine = sa.create_engine("mysql+mysqldb://root:B3njamin178@localhost:3306/sakila", echo=True)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/hello/<name>")
def hello_there(name):
    return "Hello there " + name

@app.route("/films")
def films():
    with engine.connect() as conn:
        result = conn.execute(sa.text("SELECT * FROM film"))
        for row in result:
            print(row)
    return "Printed all films to the console!"
