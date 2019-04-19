from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, data):
        self.title = data.get('title')
        self.description = data.get('description')

    def __repr__(self):
        return '<Book {book_id}>'.format(book_id=self.book_id)

    def __str__(self):
        return json.dumps({
            'book_id': self.book_id,
            'title': self.title,
            'description': self.description
        })

    def serialize(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'description': self.description
        }


def insert(data):
    try:
        book = Book(data)
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.book_id)
    except Exception as e:
        return(str(e))


def update(book_id, data):
    try:
        book = Book.query.get(book_id)
        if book is None:
            raise Exception("data not found")
        for key, val in data.items():
            if val is not None:
                setattr(book, key, val)
        db.session.commit()
        return "Book updated. book id={}".format(book.book_id)
    except Exception as e:
        return(str(e))


def query(book_id=None):
    try:
        if book_id is None:
            books = Book.query.all()
            return {"results": [book.serialize() for book in books]}
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            raise Exception("data not found")
        return book.serialize()
    except Exception as e:
        return(str(e))


def delete(book_id):
    try:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return "Book deleted. book id={}".format(book.book_id)
    except Exception as e:
        return(str(e))
