import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user

    with open('seed_data/u.user') as u:
        reader = csv.reader(u, delimiter="|")
        for row in reader:
            age = row[1]
            age= age.decode("latin-1")
            zipcode= row[4]
            zipcode= zipcode.decode("latin-1")
            new_user= model.User(age=age, zipcode=zipcode)
            session.add(new_user)

    return session.commit()


def load_movies(session):
    # use u.item
    with open('seed_data/u.item') as i:
        reader = csv.reader(i, delimiter="|")
        for row in reader:
            if row[2] == "":
                release_date= None
            else:
                release_date = row[2].decode("latin-1")
                release_date = datetime.strptime(release_date, '%d-%b-%Y')

            name = row[1]
            name = name.decode("latin-1")

            imdb_url = row[4]
            imdb_url = imdb_url.decode("latin-1")
            new_movie = model.Movie(name=name, release_date=release_date, imdb_url=imdb_url)
            session.add(new_movie)

    return session.commit()

def load_ratings(session):
    # use u.data

    with open('seed_data/u.data') as d:
        reader = csv.reader(d, delimiter="\t") 
        for row in reader:
            movie_id = row[1]
            movie_id = movie_id.decode("latin-1")
            user_id = row[0]
            user_id = user_id.decode("latin-1")
            rating = row[2]
            rating = rating.decode("latin-1")
            new_rating = model.Rating(movie_id=movie_id, user_id=user_id, rating=rating)
            session.add(new_rating)

    return session.commit()

def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)
# You'll call each of the load_* functions with the session as an argument
    return

if __name__ == "__main__":
    s=model.connect()
    main(s)
