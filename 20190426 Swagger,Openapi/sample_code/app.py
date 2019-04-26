from flask import Flask
from flask_restplus import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app, version='1.0', title='Book Api', description='An Api for Books')

books = {}


parser = api.parser()
parser.add_argument('title', type=str, location='json')
parser.add_argument('description', type=str, location='json')



class Book(Resource):

    def get(self, book_id):
        # GET http://[hostname]/api/books/[book_id] 取得書本資料
        if book_id in books:
            return {book_id: books[book_id]}
        return {"message": "book_id doesn't exist."}

    @api.doc(parser=parser)
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


api.add_resource(Book, '/api/books/<int:book_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8899', debug=True)
