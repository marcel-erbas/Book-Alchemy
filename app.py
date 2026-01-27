from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Handles displaying the form (GET) and adding a new author (POST)."""
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        new_author = Author(
            name=name,
            birth_date=birth_date if birth_date else None,
            date_of_death=date_of_death if date_of_death else None
        )

        db.session.add(new_author)
        db.session.commit()

        return "Author added successfully!"

    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handles displaying the form with a list of authors (GET) and adding a new book linked to an author (POST)."""
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year) if publication_year else None,
            author_id=int(author_id)
        )

        db.session.add(new_book)
        db.session.commit()
        return "Book added successfully! <a href='/add_book'>Add another one</a>"

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

@app.route('/')
@app.route('/')
def home():
    """Fetches all books and allows sorting by title or author name."""
    sort_by = request.args.get('sort_by', 'title')

    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()

    return render_template('home.html', books=books)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)














""" 
with app.app_context():
    db.create_all()
"""
