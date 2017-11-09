from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

''''
create engines for the db instance


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kaijuan@localhost/bookdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
'''

'''
create the db structures
'''

db = SQLAlchemy()


association_books_authors = db.Table('books_authors',
    db.Column('books_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('authors_id', db.Integer, db.ForeignKey('authors.id'))
)

association_books_publishers = db.Table('books_publishers',
    db.Column('books_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('publishers_id', db.Integer, db.ForeignKey('publishers.id'))
)

association_authors_publishers = db.Table('authors_publishers',
    db.Column('authors_id', db.Integer, db.ForeignKey('authors.id')),
    db.Column('publishers_id', db.Integer, db.ForeignKey('publishers.id'))
)


class Base(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
# Base=declarative_base()

class Publishers(Base):
	__tablename__ = 'publishers'
	name = db.Column(db.String(300), unique=True)
	wikipedia_url = db.Column(db.String(300))
	description = db.Column(db.String(1000))
	owner = db.Column(db.String(300))
	founded = db.Column(db.String(100))
	location = db.Column(db.String(200))
	image_url = db.Column(db.String(300))
	website = db.Column(db.String(500))

	def __repr__(self):
		return self.name

class Authors(Base):
	__tablename__ = 'authors'
	name = db.Column(db.String(30), unique=True)
	born = db.Column(db.String(30))
	education = db.Column(db.String(100))
	nationality = db.Column(db.String(20))
	description = db.Column(db.String(500))
	alma_mater = db.Column(db.String(100))
	wikipedia_url = db.Column(db.String(300))
	image_url = db.Column(db.String(300))

	publishers = db.relationship('Publishers', secondary = association_authors_publishers, lazy='subquery', backref = db.backref("authors", lazy=True))

	def __repr__(self):
		return self.name

class Books(Base):
	__tablename__ = 'books'
	google_id = db.Column(db.String(12), unique=True)
	title = db.Column(db.String(30), unique=True)
	publication_date = db.Column(db.String(30))
	image_url = db.Column(db.String(300))
	description = db.Column(db.String(500))
	digest = db.Column(db.String(100))

	authors = db.relationship('Authors', secondary = association_books_authors, lazy='subquery', backref = db.backref("books", lazy=True))
	publishers = db.relationship('Publishers', secondary = association_books_publishers, lazy='subquery', backref = db.backref("books", lazy=True))

	def __repr__(self):
		return self.title

