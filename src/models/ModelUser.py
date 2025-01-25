from .entities.User import User

class ModelUser():
    
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