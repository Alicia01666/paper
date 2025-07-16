import sql_model
import schemas
import string
import random
import os
from cryptography.fernet import Fernet  
from sqlalchemy.orm import Session

def generate_key():
    """
    Generates a key and save it into a file
    """
    print("------------------------------------------------------------")
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

#This is the keys for encryption
if os.stat("secret.key").st_size == 0:
    generate_key()          #generates key only if the file is empty

Key = load_key()
print(Key)
f = Fernet(Key)

#function to display user details based on the api key
def get_user_by_api(db: Session, api_key: str):
    result = db.query(sql_model.User).with_entities(sql_model.User.api_key).all()
    for i in result:
        dec = f.decrypt(i[0])
        dec1 = dec.decode()
        if dec1 == api_key:
            return db.query(sql_model.User).filter(sql_model.User.api_key == i[0]).first()
        

def get_user_by_username(db: Session, username: str):
    return db.query(sql_model.User).filter(sql_model.User.username == username).first()


#function to create an entry in the table which returns the api key
def create_user(db: Session, user: schemas.UserCreate):
    key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10)) 
    api_key1 = f.encrypt(key.encode())
    db_user = sql_model.User(username = user.username, email = user.email, api_key = api_key1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    api = db_user.api_key
    return f.decrypt(api)

#function to list all the keys in the database
def get_keys(db: Session):
    result = db.query(sql_model.User).with_entities(sql_model.User.api_key).all()
    lis = []
    for r in result:
        dec = f.decrypt(r[0])
        dec1 = dec.decode()
        lis.append(dec1)
    return lis
        
