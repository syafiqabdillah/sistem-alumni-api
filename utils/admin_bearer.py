from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth import read_jwt

class AdminBearer(HTTPBearer):
  def __init__(self, auto_error: bool = True):
    super(AdminBearer, self).__init__(auto_error=auto_error)

  async def __call__(self, request: Request):
    credentials: HTTPAuthorizationCredentials = await super(AdminBearer, self).__call__(request)
    if credentials:
      if not credentials.scheme == "Bearer":
        raise HTTPException(403, "Invalid authentication scheme")
      if not self.verify_jwt(credentials.credentials):
        raise HTTPException(403, "Invalid or expired token")
      return credentials.credentials
    else:
      raise HTTPException(403, 'Invalid code')
  
  def verify_jwt(self, jwttoken: str) -> bool:
    isTokenValid: bool = False

    try:
      payload = read_jwt(jwttoken)
    except:
      payload = None
    if payload:
      isTokenValid = payload['is_admin']
    return isTokenValid