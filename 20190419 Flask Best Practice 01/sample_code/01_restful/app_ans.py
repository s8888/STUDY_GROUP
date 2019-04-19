from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

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
        super(BookList, self).__init__()

    def get(self):
        # GET http://[hostname]/api/books 取得書本清單
        return books

    def post(self):
        # POST http://[hostname]/api/books 建立新的書本
        args = self.reqparse.parse_args()
        book_id = args.book_id
        if args.book_id in books:
            return {"message": "book_id already exists."}
        books[args.book_id] = args
        return {book_id: books[book_id]}


class Book(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(Book, self).__init__()

    def get(self, book_id):
        # GET http://[hostname]/api/books/[book_id] 取得書本資料
        if book_id in books:
            return {book_id: books[book_id]}
        return {"message": "book_id doesn't exist."}

    def put(self, book_id):
        # PUT http://[hostname]/api/books/[book_id] 更新書本資料
        if book_id in books:
            args = self.reqparse.parse_args()
            for key, val in args.items():
                if val is not None:
                    books[book_id][key] = val
            return {book_id: books[book_id]}
        return {"message": "book_id doesn't exist."}

    def delete(self, book_id):
        # DELETE http://[hostname]/api/books/[book_id] 刪除書本
        if book_id in books:
            del books[book_id]
            return {"message": "delete success"}
        return {"message": "book_id doesn't exist."}


api.add_resource(BookList, '/api/books/')
api.add_resource(Book, '/api/books/<int:book_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8899', debug=True)
