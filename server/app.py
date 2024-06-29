#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask import Flask, jsonify, request

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get('/restaurant')
def all_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_dicts = {restaurant.to_dicts() for restaurant in restaurants}
    return jsonify(restaurant_dicts), 200

@app.get('/pizzas')
def all_pizzas():
    pizzas = Pizza.query.all()
    pizzas_list = list(map(lambda pizza: pizza.to_dict(rules=["-restaurant_pizzas"]), pizzas))
    return jsonify(pizzas_list)

@app.route('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.to_dict(rules=["-restaurant_pizzas.restaurant"]))


if __name__ == "__main__":
    app.run(port=5555, debug=True)
