import model
import csv

def load_users(session):
    # use u.user

    with open('seed_data/u.user') as u:
        reader = csv.reader(u, delimiter="|")
        for row in reader:
            new_user=row[0], row[1], row[4]
            #new_user = Userid, age, zipcode
    return

s = model.connect()
load_users(s)


# def load_movies(session):
#     # use u.item
#     pass

# def load_ratings(session):
#     # use u.data
#     pass

# def main(session):
# # You'll call each of the load_* functions with the session as an argument
#     return

# if __name__ == "__main__":
#     s= model.connect()
#     main(s)
