from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import identity, authenticate


app = Flask(__name__)
api = Api(app)
app.secret_key = 'pankaj' #This must be long and unique

jwt = JWT(app=app,
          identity_handler=identity,
          authentication_handler=authenticate)

items = []

@app.route('/')
def home():
    return "Welcome to REST API"


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": "Item already added"}, 400

        request_data = request.get_json()
        price = request_data['price']
        new_item = {'name': name, 'price': price}
        items.append(new_item)
        return new_item, 201

    @jwt_required()
    def delete(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None:
            items.remove(item)
            return {"message": "Item removed successfully", 'item': item}
        else:
            return {"message": "No record found"}, 404

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        request_data = request.get_json()
        price = request_data['price']
        if item is not None:
            item['price'] = price
            return item
        else:
            new_item = {'name': name, 'price': price}
            items.append(new_item)
            return new_item

class Items(Resource):
    def get(self):
        return items


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
app.run(debug=True)
