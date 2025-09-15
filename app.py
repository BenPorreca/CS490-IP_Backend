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

@app.route("/script1")
def script1():
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            select 	film.film_id, 
                    film.title, 
                    category.name 
            from film 
            join film_category on film.film_id = film_category.film_id
            join category on film_category.category_id = category.category_id;
        """))
        for row in result:
            print(row)
    return "Display film id, title, and film category name"

@app.route("/top5films")
def script2():
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            select f.film_id,
                    f.title,
                    c.name,
                    count(i.film_id) as rental_count
            from rental r
            join inventory i on r.inventory_id = i.inventory_id 
            join film f on i.film_id = f.film_id 
            join film_category fc on f.film_id = fc.film_id 
            join category c on fc.category_id = c.category_id 
            group by f.film_id, f.title, c.name
            order by rental_count desc
            limit 5;
        """))
        for row in result:
            print(row)
    return "TOP 5 FILMS"