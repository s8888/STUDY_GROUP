from flask import Flask
from flask_restful import Resource, Api, reqparse
from models import db
import models
from config import config
import os

app = Flask(__name__)
config_name = os.environ.get('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])
db.init_app(app)
api = Api(app)


class BookList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No title provided', location='json')
        self.reqparse.add_argument(
            'description', type=str, default="", location='json')
        # TODO 增加 author, isbn
        super(BookList, self).__init__()

    def get(self):
        # GET http://[hostname]/api/books 取得書本清單
        return models.query()

    def post(self):
        # POST http://[hostname]/api/books 建立新的書本
        args = self.reqparse.parse_args()
        return models.insert(args)


class Book(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        # TODO 增加 author, isbn
        super(Book, self).__init__()

    def get(self, book_id):
        # GET http://[hostname]/api/books/[book_id] 取得書本資料
        return models.query(book_id)

    def put(self, book_id):
        # PUT http://[hostname]/api/books/[book_id] 更新書本資料
        args = self.reqparse.parse_args()
        return models.update(book_id, args)

    def delete(self, book_id):
        # DELETE http://[hostname]/api/books/[book_id] 刪除書本
        return models.delete(book_id)


api.add_resource(BookList, '/api/books/')
api.add_resource(Book, '/api/books/<string:book_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8899', debug=True)
