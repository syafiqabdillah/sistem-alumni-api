from utils.db import write, read
from utils.auth import generate_id, get_current_time, hash_password, password_matches, create_jwt, read_jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import json
import datetime

BASE_QUERY = """
            SELECT %s
            FROM users 
            """
FIELDS = [
    'id',
    'email',
    'fullname',
    'birthplace',
    'birthdate',
    'gender',
    'phone',
    'address',
    'parent_name',
    'parent_phone',
    'year_entry_tk',
    'year_entry_sd',
    'year_entry_smp',
    'year_entry_sma',
    'activity',
    'created_date',
    'updated_date',
    'is_admin',
    'verified_date',
    'verified_by'
]
PARSED_QUERY = BASE_QUERY % (', '.join(FIELDS))


def create(
        password,
        email,
        fullname,
        birthplace,
        birthdate,
        gender,
        phone,
        address,
        parent_name,
        parent_phone,
        year_entry_tk,
        year_entry_sd,
        year_entry_smp,
        year_entry_sma,
        activity):
    VALUES_TEMPLATE = ", ".join(['%s' for i in range(0, 18)])
    query = """
            INSERT INTO users (
                hashed_password,
                id,
                email,
                fullname,
                birthplace,
                birthdate,
                gender,
                phone,
                address,
                parent_name,
                parent_phone,
                year_entry_tk,
                year_entry_sd,
                year_entry_smp,
                year_entry_sma,
                activity,
                created_date,
                updated_date
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """
    id = generate_id()
    created_date = get_current_time()
    hashed_password = hash_password(password)
    write(query, (
        hashed_password,
        id,
        email,
        fullname,
        birthplace,
        birthdate,
        gender,
        phone,
        address,
        parent_name,
        parent_phone,
        year_entry_tk,
        year_entry_sd,
        year_entry_smp,
        year_entry_sma,
        activity,
        created_date,
        created_date
    ))
    return getByEmail(email)


def getByEmail(email):
    condition = "WHERE email = '%s'" % (email, )
    results = read(PARSED_QUERY + condition)
    if len(results) == 0:
        raise HTTPException(404)
    user = results[0]
    response_body = {}
    for i in range(len(FIELDS)):
        response_body[FIELDS[i]] = jsonable_encoder(user[i])
    return response_body


def login(email, password):
    query = """
          SELECT hashed_password
          FROM users 
          WHERE email = '%s'
          """
    parsed_query = query % (email, )
    try:
        results = read(parsed_query)
        if len(results) == 0:
            raise HTTPException(404)
        else:
          hashed_password = results[0][0].encode()
          if not password_matches(password, hashed_password):
            raise HTTPException(403)
          else:
            user = getByEmail(email)
            jwt = create_jwt(user)
            return jwt
    except Exception as e:
      print(e)
      raise HTTPException(500, e)


def resultsToObjects(results):
    obj_list = []
    for result in results:
        obj = {}
        for i in range(len(FIELDS)):
            obj[FIELDS[i]] = result[i]
        obj_list.append(obj)
    return obj_list


def getAll():
    results = read(PARSED_QUERY)
    return resultsToObjects(results)

def verify(email, jwt):
    jwtContent = read_jwt(jwt)
    query = """
            UPDATE users
            SET
            verified_date = %s,
            verified_by = %s
            WHERE
            email= %s
            """
    verified_date = get_current_time()
    result = write(query, (verified_date, jwtContent['email'], email))
    return {
        "message": "Verification success"
    }

def update(data):
  form = data
  jwt = form.pop('jwt')
  updated_by = read_jwt(jwt)['email']
  updated_date = get_current_time()
  query = """
          UPDATE users 
          SET
          fullname = %s,
          birthplace = %s,
          birthdate = %s,
          gender = %s,
          phone = %s,
          address = %s,
          parent_name = %s,
          parent_phone = %s,
          year_entry_tk = %s,
          year_entry_sd = %s,
          year_entry_smp = %s,
          year_entry_sma = %s,
          activity = %s,
          updated_by = %s,
          updated_date = %s,
          is_admin = %s
          WHERE 
          email = %s
          """
  result = write(query, (
    form['fullname'],
    form['birthplace'],
    form['birthdate'],
    form['gender'],
    form['phone'],
    form['address'],
    form['parent_name'],
    form['parent_phone'],
    int(form['year_entry_tk']) if form['year_entry_tk'] else None,
    int(form['year_entry_sd']) if form['year_entry_sd'] else None,
    int(form['year_entry_smp']) if form['year_entry_smp'] else None,
    int(form['year_entry_sma']) if form['year_entry_sma'] else None,
    form['activity'],
    updated_by,
    updated_date,
    int(form['is_admin']),
    form['email']
  ))
  return result

def changePassword(data):
    try:
        email = data['email']
        oldPassword = data['old_password']
        newPassword = data['new_password']
        query = f"SELECT hashed_password FROM users WHERE email = '{email}'"
        hashedPassword = read(query)[0][0].encode()
        if password_matches(oldPassword, hashedPassword):
            newHashedPassword = hash_password(newPassword)
            query = "UPDATE users SET hashed_password = %s WHERE email = %s"
            result = write(query, (newHashedPassword, email))
            return result
        raise HTTPException(403)
    except Exception as e:
        print(e)
        raise HTTPException(500)