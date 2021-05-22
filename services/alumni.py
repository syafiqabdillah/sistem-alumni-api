from utils.db import write, read
from utils.auth import generate_id, get_current_time, hash_password, password_matches, create_jwt, read_jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import json
import datetime
import math

def getAlumniCount(unit):
  query = """
          SELECT count(1) 
          FROM users 
          WHERE 
          year_entry_%s IS NOT NULL AND 
          verified_date IS NOT NULL
          """
  count = read(query % unit)[0][0]
  return {
    "count": count
  }

LIMIT = 6

def getAlumni(unit, page, query):
  # Limited data
  like = f"%{query.lower()}%"
  offset = math.floor((page - 1) * LIMIT)
  query = """
          SELECT id, email, fullname, profile_picture, year_entry_%s
          FROM users
          WHERE 
          year_entry_%s IS NOT NULL AND 
          verified_date IS NOT NULL AND 
          email != 'syafiq.abdillah@ui.ac.id' AND
          LOWER(fullname) like '%s'
          ORDER BY year_entry_%s ASC
          LIMIT %s
          OFFSET %s
          """
  results = read(query % (unit, unit, like, unit, LIMIT, offset))
  users = [
    {
      "id": alumni[0],
      "email": alumni[1],
      "fullname": alumni[2],
      "profile_picture": alumni[3],
      "year_entry": alumni[4]
    } for alumni in results
  ]
  # All data
  query = """
          SELECT count(1)
          FROM users
          WHERE 
          year_entry_%s IS NOT NULL AND 
          verified_date IS NOT NULL AND 
          email != 'syafiq.abdillah@ui.ac.id' AND
          LOWER(fullname) like '%s'
          """
  parsed = query % (unit, like)
  totalData = read(parsed)[0][0]
  totalPage = math.ceil(totalData / LIMIT)
  result = {
    'users': users,
    'pagination': {
      'currentPage': page,
      'totalData': totalData,
      'perPage': LIMIT,
      'totalPage': totalPage,
      'nextPage': page + 1 if page < totalPage else None,
      'prevPage': page - 1 if page > 1 else None
    }
  }
  return result

def checkVerifiedAlumni(jwt):
  jwtContent = read_jwt(jwt)
  email = jwtContent['email']
  query = "SELECT count(1) FROM users WHERE email = '%s' AND verified_date IS NOT NULL"
  result = read(query % email)[0][0]
  return {
    "verified": result == 1
  }