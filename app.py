from flask import Flask, jsonify
import sqlalchemy as sa

engine = sa.create_engine("mysql+mysqldb://root:B3njamin178@localhost:3306/sakila", echo=True)
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

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
        data = [dict(row._mapping) for row in result]
    return jsonify(data)

@app.route("/top5actors")
def script3():
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            select 	a.actor_id,
                    a.first_name,
                    a.last_name,
                    count(fa.film_id) as film_count
            from actor a 
            join film_actor fa on a.actor_id = fa.actor_id 
            group by a.actor_id, a.first_name, a.last_name 
            order by film_count desc
            limit 5;
        """))
        data = [dict(row._mapping) for row in result]
    return jsonify(data)

@app.route("/actorInfo/<actor>")
def script4(actor):
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            select f.film_id,
                    f.title,
                    count(r.rental_id) as rental_count
            from rental r
            join inventory i on r.inventory_id  = i.inventory_id 
            join film f on i.film_id = f.film_id
            join film_actor fa on f.film_id = fa.film_id 
            where fa.actor_id = :actor_id
            group by f.film_id, f.title 
            order by rental_count desc
            limit 5;
        """), {"actor_id": actor})
        data = [dict(row._mapping) for row in result]
    return jsonify(data)