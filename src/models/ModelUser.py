from .entities.User import User
import os
import pandas as pd

class ModelUser():

    movies = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "movies.csv"))
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()

            sql = """SELECT id, username, password,fullname FROM users WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1], User.check_password(row[2], user.password),row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        


    @classmethod
    def register(self,db, user):
        try:
            cursor = db.connection.cursor()

            sql = """INSERT INTO users (username, password, fullname)
            VALUES (%s, %s, %s)"""

            values = (user[0], user[1], user[2])

            cursor.execute(sql, values)

            db.connection.commit()  

        except Exception as ex:

            db.connection.rollback()  
            raise ex
        
        finally:
            cursor.close()
            

    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT id, username, fullname FROM users WHERE id = {} ".format(id)

            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def filter_by_genres(cls,selected_genres):
        filtered_movies = cls.movies[cls.movies['genres'].apply(
            lambda x: all(genre.strip() in x for genre in selected_genres)
        )]
        return filtered_movies[['title', 'genres']].head(1000).to_dict(orient='records')