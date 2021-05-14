from utils.db import write, read
from utils.auth import generate_id, get_current_time, hash_password, password_matches, create_jwt, read_jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import json
import datetime

def getAlumniCount(unit):
  count = read("SELECT count(1) FROM users WHERE year_entry_%s IS NOT NULL" % unit)[0][0]
  return {
    "count": count
  }

def getAlumni(unit):
  query = """
          SELECT email, fullname
          FROM users
          WHERE year_entry_%s IS NOT NULL
          AND verified_date IS NOT NULL
          """
  results = read(query % unit)
  return [
    {
      "email": alumni[0],
      "fullname": alumni[1]
    } for alumni in results
  ]

def checkVerifiedAlumni(jwt):
  jwtContent = read_jwt(jwt)
  email = jwtContent['email']
  query = "SELECT count(1) FROM users WHERE email = '%s' AND verified_date IS NOT NULL"
  result = read(query % email)[0][0]
  return {
    "verified": result == 1
  }