from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

'''
books = {'[book_id]': {
    book_id: [book_id],
    title: [title],
    description: [description]
}}
'''
books = {}


class BookList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('book_id', type=int, required=True,
                                   help='No book_id provided', location='json')
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No title provided', location='json')
        self.reqparse.add_argument(
            'description', type=str, default="", location='json')
        # useage: args = self.reqparse.parse_args()
        super(BookList, self).__init__()

    def get(self):
        # GET http://[hostname]/api/books 取得書本清單
        # TODO
        pass

    def post(self):
        # POST http://[hostname]/api/books 建立新的書本
        # TODO
        pass


class Book(Resource):
    def __init__(self):
        # TODO
        pass

    def get(self, book_id):
        # GET http://[hostname]/api/books/[book_id] 取得書本資料
        # TODO
        pass

    def put(self, book_id):
        # PUT http://[hostname]/api/books/[book_id] 更新書本資料
        # TODO
        pass

    def delete(self, book_id):
        # DELETE http://[hostname]/api/books/[book_id] 刪除書本
        # TODO
        pass


api.add_resource(BookList, '/api/books/')
api.add_resource(Book, '/api/books/<int:book_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8899', debug=True)
