import os
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from .entities.User import User

class ModelUser:
    movies = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "movies.csv"))
    
    @classmethod
    def login(cls, supabase_client, user):
        try:
            response = supabase_client.table("users").select("id, username, password, fullname").eq("username", user.username).execute()
            if response.data:
                row = response.data[0]
                if check_password_hash(row["password"], user.password):  # Verificar la contraseña
                    return User(row["id"], row["username"], True, row["fullname"])
                else:
                    return User(row["id"], row["username"], False, row["fullname"])
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error during login: {ex}")

    @classmethod
    def register(cls, supabase_client, user):
        try:
            hashed_password = generate_password_hash(user[1])  # Generar hash de la contraseña

            response = supabase_client.table("users").insert({
                "username": user[0],
                "password": hashed_password,
                "fullname": user[2],
            }).execute()

       
            print("Registro exitoso:", response.data)  
        except Exception as ex:
            
            print(f"Error durante el registro: {ex}")
            raise Exception(f"Error durante el registro: {ex}")

    @classmethod
    def get_by_id(cls, supabase_client, id):
        try:
            # Consultar usuario por ID en Supabase
            response = supabase_client.table("users").select("id, username, fullname").eq("id", id).execute()
            if response.data:
                row = response.data[0]
                return User(row["id"], row["username"], None, row["fullname"])
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error fetching user by ID: {ex}")

    @classmethod
    def filter_by_genres(cls, selected_genres):
        try:
           
            filtered_movies = cls.movies[cls.movies["genres"].apply(
                lambda x: all(genre.strip() in x for genre in selected_genres)
            )]
            return filtered_movies[["title", "genres"]].head(1000).to_dict(orient="records")
        except Exception as ex:
            raise Exception(f"Error filtering movies: {ex}")