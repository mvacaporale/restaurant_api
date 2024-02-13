from flask import Flask
from flask_restful import Resource, Api, reqparse

from restaurants.data import RestaurantData
from restaurants.utils import is_isoformat, ISOFORMAT

app = Flask(__name__)
api = Api(app)


class Restaurants(Resource):

    def __init__(self, data):
        self.restaurant_data = data

    def get(self):

        # Add one argument for a datetime str.
        parser = reqparse.RequestParser()
        parser.add_argument("datetime", location="args", required=True)
        args = parser.parse_args()

        # Validate datetime input format.
        datetime = args['datetime']
        if not is_isoformat(datetime):
            return {
                "message": f"Invalid datetime format. Should be '{ISOFORMAT}'. "
                           f"Instead received '{datetime}'."
            }, 400

        # Return list of open restaurants at the given date and time.
        all_open = self.restaurant_data.get_open_restaurants(datetime)
        return {"data": all_open}, 200


data = RestaurantData()
api.add_resource(
    Restaurants, "/restaurants",
    resource_class_kwargs={"data": data}
)
