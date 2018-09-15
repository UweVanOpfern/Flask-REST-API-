from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.stores import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="The field name is price and make sure you fill it")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs store id")

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store with this name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db() # Save into database

        except 'Exception':

            return {"message": "Error occurred while inserting store"}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}
