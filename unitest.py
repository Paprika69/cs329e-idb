from unittest import TestCase, main
from models import  Base, Books, Publishers, Authors
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask
import os

# def setup_module():
#     global engine, transaction, connection
#     engine=create_engine('postgresql://postgres:Kaijuan@localhost/bookdb')
#     connection=engine.connect()
#     transaction=connection.begin()
#     Base.metadata.create_all(connection)


class DBTestCases(TestCase):
    DB_PATH = os.path.join(os.path.dirname(__file__), 'book_test.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///{}'.format(DB_PATH))
    engine=create_engine(SQLALCHEMY_DATABASE_URI)

    Session=sessionmaker(bind=engine)
    session=Session()

    def setUp(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self.author_1=Authors(name='Nason Alex',born='1943-03-26',nationality='American',education='Yale University, BA, 1965',description='investigative journalist',wikipedia_url='https://en.wikipedia.org/wiki/Bob_Woodward',image_url='http://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Bob_Woodward.jpg/220px-Bob_Woodward.jpg')
        self.author_2=Authors(name='Patrick Rothfuss',born='1994-08-13',nationality='Chinese',image_url="http://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Patrick-rothfuss-2014-kyle-cassidy.jpg/250px-Patrick-rothfuss-2014-kyle-cassidy.jpg")
        self.author_3=Authors(name='Robin Hortz',nationality='Australian',born='1952-03-05')
        self.publisher_1=Publishers(name='Simon & Schuster',founded='1924',wikipedia_url= "https://en.wikipedia.org/wiki/Simon_%26_Schuster",website= "http://www.simonandschuster.com")
        self.publisher_2=Publishers(name='HarperCollins',founded='1989',location='New York',website='http://harpercollins.com')
        self.publisher_3=Publishers(name='Penguin Group',founded='1935',location='City of Westminster, London')

        self.book_1=Books(title='Royal Assassin',google_id='kx12345',publication_date='2003-04-05')
        self.book_1.authors.append(self.author_3)

        self.book_2=Books(title='Under the sea',google_id='34567',publication_date='2017-09-21')
        self.book_2.publishers.append(self.publisher_1)

        self.author_2.publishers.append(self.publisher_2)

        self.session.add(self.author_1)
        self.session.add(self.author_2)
        self.session.add(self.author_3)
        self.session.add(self.publisher_1)
        self.session.add(self.publisher_2)
        self.session.add(self.publisher_3)
        self.session.add(self.book_1)
        self.session.add(self.book_2)
        self.session.commit()

    # def tearDown(self):


    def test_author_1(self):
        result=self.session.query(Authors).filter_by(name='Nason Alex').one()
        self.assertEqual(str(result.born),'1943-03-26')


        self.session.query(Authors).filter_by(name='Nason Alex').delete()
        self.session.commit()


    def test_author_2(self):
        updated_nationality=self.session.query(Authors).filter_by(name='Patrick Rothfuss').update({'nationality':'British'},synchronize_session=False)
        result=self.session.query(Authors).filter_by(name='Patrick Rothfuss').one()
        self.assertEqual(str(result.nationality),'British')

        self.session.commit()

    def test_author_3(self):
        author_count_before=self.session.query(Authors).count()
        # self.assertEqual(author_count_before,3)
        self.author_4=Authors(name='Orson Scott Card',born='1950',nationality='American',wikipedia_url='https://en.wikipedia.org/wiki/Orson_Scott_Card')
        self.session.add(self.author_4)

        author_count_now=self.session.query(Authors).count()
        self.assertEqual(author_count_now,author_count_before+1)

        self.session.delete(self.author_4)
        self.session.commit()

    def test_publisher(self):
        publisher_result=self.session.query(Publishers).filter_by(founded="1924").one()
        self.assertEqual(str(publisher_result.name),'Simon & Schuster')

        self.session.commit()

    def test_publisher_2(self):
        publisher_count=self.session.query(Publishers).count()
        self.assertEqual(publisher_count,3)
        self.session.commit()

    def test_book(self):
        result=self.session.query(Books).filter_by(title='Under the sea').one()
        self.assertEqual(str(result.google_id),'34567')
        self.session.commit()


    def test_book_author(self):
        result=self.session.query(Books).filter_by(title='Royal Assassin').one()
        self.assertEqual(str(result.authors[0].nationality),'Australian')

        self.session.delete(self.book_1)
        self.session.delete(self.author_3)
        self.session.commit()

    def test_book_publisher(self):
        result=self.session.query(Books).filter_by(title='Under the sea').one()
        self.assertEqual(str(result.publishers[0]),'Simon & Schuster')

        self.session.delete(self.book_2)
        self.session.delete(self.publisher_1)
        self.session.commit()

    def test_author_publisher(self):
        result=self.session.query(Authors).filter_by(name='Patrick Rothfuss').one()
        self.assertEqual(str(result.publishers[0]),'HarperCollins')

        self.session.delete(self.author_2)
        self.session.delete(self.publisher_2)
        self.session.commit()
    def test_delete_books_1(self):
        self.session.add(Books(title='1999',google_id='34167',publication_date='2017-04-21'))
        self.session.commit()

        query = self.session.query(Books).filter_by(title ="1999").first()

        self.assertTrue(str(query.title),"1999")
        self.session.query(Books).filter_by(title='1999').delete()
        self.session.commit()
        number = self.session.query(Books).filter_by(title='1999').count()
        self.assertTrue(str(number),"0")
    def test_delete_authors(self):
        self.session.add(Authors(name='Benjamin',born='1998-08-13',nationality='Chinese',image_url="http://upload.wikimedia.org/wikipedia/commons/thumbs/"))
        self.session.commit()

        query = self.session.query(Authors).filter_by(born ="1998-08-13").first()

        self.assertTrue(query.born,"1998-08-13")
        self.session.query(Authors).filter_by(born ="1998-08-13").delete()
        self.session.commit()
        number = self.session.query(Authors).filter_by(born ="1998-08-13").count()
        self.assertTrue(str(number),"0")
    def test_delete_publishers(self):
        self.session.add(Publishers(name='Renmin Chubanshe',founded='1855',wikipedia_url= "https://en.wikipedia.org/wiki/"))

        query = self.session.query(
            Publishers).filter_by(
            founded="1855").first()

        self.assertTrue(query.founded,"1855")
        self.assertTrue(query.name, "Renmin Chubanshe")
        self.session.query(Publishers).filter_by(
            founded="1855").delete()
        self.session.commit()
        number = self.session.query(
            Publishers).filter_by(
            founded="1855").count()
        self.assertTrue(str(number), "0")
    # test filtering multiple publishers which shares the same attributes
    def test_publishers_2(self):
        self.session.add(Publishers(name="Tencent", founded="1998",wikipedia_url="www.qq.com" ))
        self.session.add(Publishers(name="Thunder", founded = "1998",wikipedia_url="www.thunder.com"))
        self.session.commit()
        query = self.session.query(Publishers).filter_by(founded = "1998").all()
        foundeds = []
        for i in query:
            foundeds.append(i.founded)
        self.assertTrue(foundeds[0]== foundeds[1])
        self.session.query(Publishers).filter_by(founded = "1998").delete()
        self.session.query(Publishers).filter_by(founded = "1998").delete()
        self.session.commit()


    def test_books_update(self):
        self.session.add(Authors(name="Paprika Jiang",born = "1924-02-14",nationality='American',education='Yale University, BA, 1965'))
        self.session.query(Authors).filter_by(name='Paprika Jiang').update({'nationality': 'Chinese'},
            synchronize_session=False)
        self.session.commit()
        result = self.session.query(Authors).filter_by(name='Paprika Jiang').one()
        self.assertTrue(result.nationality,'Chinese')
        self.session.query(Authors).filter_by(name ="Paprika Jiang").delete()

        self.session.commit()

    def test_publishers_update(self):
        self.session.add(Publishers(name="GroupStars", founded="1998",wikipedia_url="www.star.com" ))
        self.session.query(Publishers).filter_by(name='GroupStars').update({'founded': '1999'},
            synchronize_session=False)
        self.session.commit()
        result = self.session.query(Publishers).filter_by(name='GroupStars').one()
        self.assertTrue(result.founded,'1999')
        self.session.query(Authors).filter_by(name ="GroupStars").delete()
        self.session.commit()

    def test_books_insert(self):
        self.session.add(Books(title='Nothing to Envy',google_id='0385523912',publication_date='2009-12-29'))
        self.session.commit()
        result = self.session.query(Books).filter_by(title='Nothing to Envy').one()
        self.assertEqual(str(result.google_id), '0385523912')
        self.assertEqual(str(result.publication_date), '2009-12-29')
        self.session.query(Books).filter_by(title='Nothing to Envy').delete()
        self.session.commit()


if __name__=='__main__':
    main()








