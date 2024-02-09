from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class Restaurants(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("datetime", location="args", required=True)
        args = parser.parse_args()

        # TODO: Handle error cases.
        # Return for error codes https://restfulapi.net/http-status-codes/

        datetime = args['datetime']
        return {"data": datetime}, 200

api.add_resource(Restaurants, '/restaurants')

if __name__ == '__main__':
    app.run()
