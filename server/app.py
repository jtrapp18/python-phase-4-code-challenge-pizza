#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
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

class RestaurantIndex(Resource):

    def get(self):
        restaurants = [
            {key: value for key, value in restaurant.to_dict().items() if key != 'restaurant_pizzas'}
            for restaurant in Restaurant.query.all()
        ]
        return restaurants, 200

    def post(self):
        data = request.get_json()

        try:
            new_restaurant = Restaurant(
                name=data['name'],
                address=data['address']
            )

            db.session.add(new_restaurant)
            db.session.commit()

            return new_restaurant.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400

class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        
        restaurant_dict = restaurant.to_dict()
        
        return restaurant_dict, 200

    def patch(self, id):
        record = Restaurant.query.filter_by(id=id).first()
        data = request.get_json()

        if not record:
            return {"error": "Restaurant not found"}, 404

        for attr in data:
            setattr(record , attr, data.get(attr))

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        return response_dict, 200
    
    def delete(self, id):

        record = Restaurant.query.filter_by(id=id).first()

        if not record:
            return {"error": "Restaurant not found"}, 404
        
        db.session.delete(record)
        db.session.commit()

        return "", 204

class PizzaIndex(Resource):

    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return pizzas, 200
    
class RestaurantPizzaIndex(Resource):

    def get(self):
        restaurant_pizzas = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]
        return restaurant_pizzas, 200

    def post(self):
        data = request.get_json()

        try:
            new_restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

            return new_restaurant_pizza.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400

api.add_resource(RestaurantIndex, '/restaurants')
api.add_resource(RestaurantByID, '/restaurants/<int:id>')
api.add_resource(PizzaIndex, '/pizzas')
api.add_resource(RestaurantPizzaIndex, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
