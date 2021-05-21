from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from typing import Optional 
from pydantic import BaseModel
from utils.auth import read_jwt
from utils.auth_bearer import JWTBearer
from utils.admin_bearer import AdminBearer
import shutil
import os
import services.users as db
import services.alumni as db_alumni
from datetime import datetime

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


@router.get('/by-email', dependencies=[Depends(JWTBearer())])
def getByEmail(email, Authorization: Optional[str] = Header(None)):
  jwt = Authorization.split(' ')[1]
  jwtContent = read_jwt(jwt)
  # valid if admin atau dirinya sendiri
  if jwtContent['is_admin'] or email == jwtContent['email']:
    return db.getByEmail(email)
  raise HTTPException(403)

class FormLogin(BaseModel):
  email: str
  password: str

@router.post('/login')
def login(form: FormLogin):
  return db.login(form.email, form.password)

@router.get('/', dependencies=[Depends(AdminBearer())])
def getAll(query: str= "", page: int = 1):
  return db.getAll(query.lower(), page)

@router.get('/unverified', dependencies=[Depends(AdminBearer())])
def getUnverified(query: str = "", page: int = 1):
  return db.getUnverified(query.lower(), page)

@router.get('/verified', dependencies=[Depends(AdminBearer())])
def getVerified(query: str = "", page: int = 1):
  return db.getVerified(query.lower(), page)

class FormVerification(BaseModel):
  email: str

@router.post('/verify', dependencies=[Depends(JWTBearer())])
def verify(form: FormVerification, Authorization: Optional[str] = Header(None)):
  jwt = Authorization.split(' ')[1]
  if read_jwt(jwt)['is_admin']:
    return db.verify(form.email, jwt)
  raise HTTPException(403)

@router.get('/alumni-count')
def getAlumniCount(unit: str):
  return db_alumni.getAlumniCount(unit)

@router.get('/alumni', dependencies=[Depends(JWTBearer())])
def getAlumni(unit: str, page: int, query: str):
  return db_alumni.getAlumni(unit, page, query)

class FormCheckVerified(BaseModel):
  jwt: str

@router.post('/check-verified')
def checkVerifiedAlumni(form: FormCheckVerified):
  return db_alumni.checkVerifiedAlumni(form.jwt)

class FormEdit(BaseModel):
  jwt: str
  email: str
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
  is_admin: bool

@router.post('/update')
def update(form: FormEdit):
  return db.update(form.dict())

class FormChangePassword(BaseModel):
  email: str
  old_password: str
  new_password: str

@router.post('/change-password', dependencies=[Depends(JWTBearer())])
def changePassword(form: FormChangePassword):
  return db.changePassword(form.dict())

class FormUploadFile(BaseModel):
  id: str  

def fileSizeValid(file):
  return file.spool_max_size / 1024 / 1024 < 2

@router.post('/upload-profile-picture', dependencies=[Depends(JWTBearer())])
async def uploadProfilePicture(id: str, file: UploadFile = File(...), Authorization: Optional[str] = Header(None)):
  if (fileSizeValid(file)):
    try:
      ext = file.filename.split('.')[-1]
      ts = int(datetime.now().timestamp())
      filename = f"{id}-{ts}.{ext}"
      with open(os.path.join('image', filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
      db.saveProfilePicture(id, filename)
      return {
        "id": id,
        "filename": filename
      }
    except Exception as e:
      print(e)
      raise HTTPException(500)
  else:
    raise HTTPException(400, 'File size too large')

@router.get('/profile-picture')
async def getProfilePicture(id: str):
  filename = db.getFilename(id)
  if filename:
    return FileResponse(os.path.join('image', filename))
  return None
