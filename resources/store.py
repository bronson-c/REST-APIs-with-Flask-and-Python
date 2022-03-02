
from importlib.resources import Resource

from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': f'Store {name} not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name {name} already exists.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': f'A database error occurred inserting store {name}'}, 500

        # 201 -> Created, 202 -> Accepted
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': f'Store {name} deleted.'}


class StoreList(Resource):
    def get(self):
        # list comprehension or lambda to get json for all items
        return {'stores': [store.json() for store in StoreModel.query.all()]}
