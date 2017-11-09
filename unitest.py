from unittest import TestCase, main
from models import  Base, Books, Publishers, Authors
from sqlalchemy.orm import sessionmaker
from test import app
from sqlalchemy import create_engine

# def setup_module():
#     global engine, transaction, connection
#     engine=create_engine('postgresql://postgres:Kaijuan@localhost/bookdb')
#     connection=engine.connect()
#     transaction=connection.begin()
#     Base.metadata.create_all(connection)
class DBTestCases(TestCase):
    engine=create_engine('postgresql://postgres:Kaijuan@localhost/bookdb')
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

    def test_publisher(self):
        publisher_result=self.session.query(Publishers).filter_by(founded="1924").one()
        self.assertEqual(str(publisher_result.name),'Simon & Schuster')

        self.session.commit()
    def test_book(self):
        result=self.session.query(Books).filter_by(title='Under the sea').one()
        self.assertEqual(str(result.google_id),'34567')
        self.session.commit()

    def test_book_author(self):
        result=self.session.query(Books).filter_by(title='Royal Assassin').one()
        self.assertEqual(str(result.authors[0].nationality),'Australian')

        self.session.commit()
    
    def test_book_publisher(self):
        result=self.session.query(Books).filter_by(title='Under the sea').one()
        self.assertEqual(str(result.publishers[0]),'Simon & Schuster')

        self.session.commit()

    def test_author_publisher(self):
        result=self.session.query(Authors).filter_by(name='Patrick Rothfuss').one()
        self.assertEqual(str(result.publishers[0]),'HarperCollins')
        self.session.commit()



if __name__=='__main__':
    main()








