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


if __name__ == "__main__":
    app.run(port=5555, debug=True)


class RestaurantIndex(Resource):

    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.filter_by(user_id=session['user_id']).all()]
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
            return {'error': 'Restaurant not valid'}, 422

class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first().to_dict()
        return make_response(restaurant, 200)

    def patch(self, id):
        record = Restaurant.query.filter_by(id=id).first()

        for attr in request.get_json():
            setattr(record , attr, request.get_json().get(attr))

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        return make_response(response_dict, 200)
    
    def delete(self, id):

        record = Restaurant.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        return make_response("", 200)

class PizzaIndex(Resource):

    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.filter_by(user_id=session['user_id']).all()]
        return restaurants, 200

    def post(self):
        data = request.get_json()

        try:
            new_pizza = Pizza(
                name=data['name'],
                ingredients=data['ingredients'],

            )

            db.session.add(new_pizza)
            db.session.commit()

            return new_pizza.to_dict(), 201
        except:
            return {'error': 'Pizza not valid'}, 422

api.add_resource(RestaurantIndex, '/restaurants')
api.add_resource(RestaurantByID, '/restaurants/<int:id>')
# api.add_resource(PizzaIndex, '/restaurants')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
