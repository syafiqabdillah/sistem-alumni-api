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
  