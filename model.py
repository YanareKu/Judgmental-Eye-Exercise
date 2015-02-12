from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, 
    autocommit = False, 
    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)


    def __repr__(self):
        return "User id = %d, email = %s, password = %s!" % (
            self.id, self.email, self.password)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = True)
    release_date = Column(DateTime, nullable = True)
    imdb_url = Column(String(100), nullable=True)

    def __repr__(self):
        return "Movie id = %d, name = %s, imdb url = %s" % (
        self.id, self.name, self.imdb_url)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    movie = relationship("Movie",
            backref=backref("ratings", order_by=id))

    user = relationship("User",
            backref=backref("ratings", order_by=id))

    def __repr__(self):
        return "Rating id = %d, movie id = %d, user id = %d, rating = %d" % (
        self.id, self.movie_id, self.user_id, self.rating)

def get_user_by_email(email_address):
    """returns a user by email address from database"""
    user = session.query(User).filter(User.email==email_address).first()

    return user

def add_user_to_db(email, password, age=None, zipcode=None):
    new_user = User(email=email, password=password, age=age, zipcode=zipcode)
    session.add(new_user)
    return session.commit()

def get_movie_names_and_ratings_by_user_id(id):
    all_ratings = session.query(Rating, Movie).outerjoin(Movie).filter(Rating.user_id==id).all()
    return all_ratings

def get_movie_rating_by_movie_name(name):
    movie_names = session.query(Movie).filter(Movie.name.like('%'+name+'%')).all()

    return movie_names

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
