import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "book.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):

    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def toJson(self):
        return {"title": self.title, 'expires-at': datetime.datetime.now() + datetime.timedelta(days=1, hours=3)}

    def __repr__(self):
        return json.dumps(self.__dict__)

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route("/books", methods=["GET"])
def index():
    books = Book.query.all()
    array_books = []
    for book in books:
        dict_books = {}
        dict_books.update({"title": book.title})
        array_books.append(dict_books)
    return jsonify(array_books), 200, {'content-type':'application/json'}        

@app.route("/books/create", methods=["POST"])
def create():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    return redirect("/")

@app.route("/books/<title>", methods=["GET"])
def show(title):
    book = Book.query.filter_by(title=title).first()
    if(book==None):
        return {"msg": "Book cant be found"}, 404
    else:
        return jsonify(book.toJson()), 200, {'content-type':'application/json'}        

@app.route("/books/update", methods=["PUT"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/books/delete", methods=["DELETE"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
   app.run(debug = True, port=4000)
