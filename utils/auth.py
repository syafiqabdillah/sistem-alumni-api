import os 
import jwt 
from dotenv import load_dotenv
import string 
import random 
import bcrypt
import pytz
from datetime import datetime
from fastapi import HTTPException

load_dotenv()

tz = pytz.timezone('Asia/Jakarta')

SECRET=os.getenv('SECRET')

def create_jwt(data):
    return jwt.encode(data, SECRET, algorithm='HS256')

def read_jwt(encoded_jwt):
    try:
        return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])
    except Exception as e:
        raise HTTPException(403, "Unauthorized")

def generate_id(length=15):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_purchase_id():
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(7))
    return result_str

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def password_matches(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def get_current_time():
    return datetime.now(tz)

if __name__=="__main__":
    print(get_current_time())