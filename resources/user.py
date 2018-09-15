import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="The field name is username and make sure you fill it")
    parser.add_argument('password', type=str, required=True,
                        help="The field name is password and make sure you fill it")

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists."}, 400  # this code indicates that it is bad request

        if data['username'] == '':
            return {"Missing field": "Username field can not be empty"}

        elif data['password'] == '':
            return {"Missing field": "Password field can not be empty"}
        else:

            user = UserModel(**data)
            user.save_to_db()

        return {"message": "User created with success"}, 201
