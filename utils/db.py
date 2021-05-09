from dotenv import load_dotenv
import mysql.connector as mysql
import os 
from fastapi import HTTPException

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

def read(query):
  try:
    with mysql.connect(
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASS,
      database=DB_NAME
    ) as connection:
      with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
  except Exception as e:
    print(e)

def write(query, value):
  print(query)
  try:
    with mysql.connect(
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASS,
      database=DB_NAME
    ) as connection:
      with connection.cursor() as cursor:
        cursor.execute(query, value)
        connection
        connection.commit()
        return True
  except Exception as e:
    print(e)
    raise HTTPException(500)