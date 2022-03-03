from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank."
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': f'Item {name} not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        # deconstruct data into [price] and [store_id] arguements
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': f'A database error occurred inserting item {name}'}, 500

        # 201 -> Created, 202 -> Accepted
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': f'Item {name} deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        # create
        if item is None:
            # deconstruct data into [price] and [store_id] arguements
            item = ItemModel(name, **data)
        # update
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # list comprehension or lambda to get json for all items
        return {'items': [item.json() for item in ItemModel.query.all()]}
