from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from .utils import is_isoformat, ISOFORMAT

app = Flask(__name__)
api = Api(app)


class Restaurants(Resource):

    def get(self):

        # Add one argument for a datetime str.
        parser = reqparse.RequestParser()
        parser.add_argument("datetime", location="args", required=True)
        args = parser.parse_args()

        # Validate datetime input format.
        datetime = args['datetime']
        if not is_isoformat(datetime):
            return {
                "message": f"Invalid datetime format. Should be {ISOFORMAT}."
            }, 400

        # Return dummy value for now.
        return {"data": ["Store 1", "Store_2"]}, 200

api.add_resource(Restaurants, '/restaurants')

if __name__ == '__main__':
    app.run()
