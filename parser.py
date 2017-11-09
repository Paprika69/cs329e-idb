import json
from models import db, Books, Authors, Publishers

def load_json(filename):
	with open(filename, 'r') as file:
		jsn = json.load(file)
		file.close()
	return jsn


def parse_json():
	jsn = load_json('books.json')
	for book in jsn:
		google_id = book.get('google_id', "")
		title = book.get('title', "")
		publication_date = book.get('publication_date', "")
		book_image_url = book.get('image_url', "")
		book_description = book.get('description', "")
		
		publishers = book.get('publishers')
		publishers_ = []
		for publisher in publishers:
			publisher_wikipedia_url = publisher.get('wikipedia_url', "")
			publisher_name = publisher.get('name', "")
			publisher_description = publisher.get('description', "")
			owner = publisher.get('owner', "")
			publisher_image_url = publisher.get('image_url', "")
			founded = publisher.get('founded', "")
			# founded and location are not belonging to every publisheres
			location = publisher.get('location', "")
			publisher_website = publisher.get('website', "")
			publishers_.append(Publishers(
				name=publisher_name,
				wikipedia_url=publisher_wikipedia_url,
				description=publisher_description,
				owner=owner,
				image_url=publisher_image_url,
				website=publisher_website,
				founded=founded,
				location=location
				))

		authors = book.get('authors')
		authors_ = []
		for author in authors:
			born = author.get('born', "")
			author_name = author.get('name', "")
			education = author.get('education', "")
			nationality = author.get('nationality', "")
			author_description = author.get('description', "")
			alma_mater = author.get('alma_mater', "")
			author_wikipedia_url = author.get('wikipedia_url', "")
			author_image_url = author.get('image_url', "")
			authors_.append(Authors(
				name=author_name, 
			    born=born,
			    education=education,
			    nationality=nationality,
			    description=author_description,
			    alma_mater=alma_mater,
			    wikipedia_url=author_wikipedia_url,
			    image_url=author_image_url,
			    ))

		yield Books(title=title, 
				google_id=google_id,
				publication_date=publication_date,
				image_url=book_image_url,
				description=book_description,
				digest=book_description,
				), \
			  	authors_, \
			  	publishers_
		
