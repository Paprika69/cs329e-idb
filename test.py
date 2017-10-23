from flask import Flask, render_template
from models import db, Books, Authors, Publishers
from parser import parse_json

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
with app.app_context():
	db.drop_all()
	db.create_all()
	get_data = parse_json()
	count = 200
	for i in range(count):
		book, authors, publishers = next(get_data, [None, None, None])
		if book is None:
			count = i+1
			break
		if not Books.query.filter_by(title=book.title).count():

			for i, author in enumerate(authors):
				if Authors.query.filter_by(name=author.name).count():
					author = Authors.query.filter_by(name=author.name).all()[0]
					authors[i] = author					
				book.authors.append(author)
				db.session.add(author)
				db.session.commit()

			for publisher in publishers:
				if Publishers.query.filter_by(name=publisher.name).count():
					publisher = Publishers.query.filter_by(name=publisher.name).all()[0]
				book.publishers.append(publisher)
				for author in authors:
					author.publishers.append(publisher)
				db.session.add(publisher)
				db.session.commit()
			db.session.add(book)
			db.session.commit()

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
	return render_template('index.html')

# make it beautiful
@app.route('/splash')
def splash():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

# @app.route('/models')
# def models():
# 	return render_template('models.html')

@app.route('/books', defaults={'book_name':None})
@app.route('/books/<book_name>')
def books(book_name):
	if book_name == None:
		books = Books.query.order_by(Books.id).all()
		return render_template('books.html', books=books)
	else:
		book = Books.query.filter_by(title=book_name).all()
		if len(book) < 1:
			return render_template('book_not_found.html', book_name=book_name)
		return render_template('book.html', book=book[0])

@app.route('/authors', defaults={'author_name':None})
@app.route('/authors/<author_name>')
def authors(author_name):
	if author_name == None:
		authors = Authors.query.order_by(Authors.id).all()
		return render_template('authors.html', authors=authors)
	else:
		author = Authors.query.filter_by(name=author_name).all()
		if len(author) < 1:
			return render_template('author_not_found.html', author_name=author_name)
		return render_template('author.html', author=author[0])

@app.route('/publishers', defaults={'publisher_name':None})
@app.route('/publishers/<publisher_name>')
def publishers(publisher_name):
	if publisher_name == None:
		publishers = Publishers.query.order_by(Publishers.id).all()
		return render_template('publishers.html', publishers=publishers)
	else:
		publisher = Publishers.query.filter_by(name=publisher_name).all()
		if len(publisher) < 1:
			return render_template('publisher_not_found.html', publisher_name=publisher_name)
		return render_template('publisher.html', publisher=publisher[0])

if __name__ == '__main__':
	app.run(debug=True);
