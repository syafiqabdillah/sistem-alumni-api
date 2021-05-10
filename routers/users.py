from fastapi import APIRouter, Depends, HTTPException
from typing import Optional 
from pydantic import BaseModel
from utils.auth import read_jwt

import services.users as db

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

class FormCreate(BaseModel):
  email: str
  password: str
  fullname: str
  birthplace: str
  birthdate: str
  gender: int
  phone: str
  address: str
  parent_name: Optional[str]
  parent_phone: Optional[str]
  year_entry_tk: Optional[str]
  year_entry_sd: Optional[str]
  year_entry_smp: Optional[str]
  year_entry_sma: Optional[str]
  activity: str

@router.post('/')
def create(form: FormCreate):
  print(form)
  return db.create(
    form.password,
    form.email,
    form.fullname,
    form.birthplace,
    form.birthdate,
    form.gender,
    form.phone,
    form.address,
    form.parent_name,
    form.parent_phone,
    form.year_entry_tk,
    form.year_entry_sd,
    form.year_entry_smp,
    form.year_entry_sma,
    form.activity
  )

@router.get('/by-email')
def getByEmail(email):
  return db.getByEmail(email)

class FormLogin(BaseModel):
  email: str
  password: str

@router.post('/login')
def login(form: FormLogin):
  return db.login(form.email, form.password)

@router.get('/')
def getAll():
  return db.getAll()

class FormVerification(BaseModel):
  email: str
  jwt: str

@router.post('/verify')
def verify(form: FormVerification):
  return db.verify(form.email, form.jwt)