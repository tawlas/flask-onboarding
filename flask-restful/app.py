from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from security import authenticate, identity
from flask_jwt import JWT, jwt_required
import requests

app = Flask(__name__)
app.secret_key = "lastaw"
api = Api(app)
jwt = JWT(app, authenticate, identity)

baseURL = "http://localhost:3001"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True,
                        help="this field cannot be left blank")
    parser.add_argument("description", type=str, required=True,
                        help="this field cannot be left blank")

    def get(self, id):
        item = requests.get(baseURL + "/posts/" + id).json()
        return {"item": item}, 200 if item is not None else 404

    def post(self, id=None):

        # if next(filter(lambda x: x["name"] == name, items)) is not None:
        #     return {"message": "Item with name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        try:
            item = requests.post(
                "http://localhost:3001/posts", json=data).json()
            return item, 201
        except:
            return {"errorMessage: There was an error when posting with post {}".format(data.title)}

    def delete(self, id):
        try:
            item = requests.delete(
                "http://localhost:3001/posts/"+id).json()
            print(item)
            return {"success": "item with id {} was successfully deleted".format(id)}, 200
        except:
            return {"errorMessage": "There was an error deleting post with id {}".format(id)}

    def put(self, id):
        data = Item.parser.parse_args()
        try:
            item = requests.put("http://localhost:3001/posts/"+id, data).json()
            return item, 200
        except:
            return {"errorMessage": "There was an error updating post with id {}".format(id)}


class ItemList(Resource):
    def get(self):
        items = requests.get(baseURL + "/posts/")
        print(items.json())
        return {"items": items.json()}


api.add_resource(Item, "/posts/<string:id>")
api.add_resource(ItemList, "/posts")

app.run(port=5000, debug=True)
