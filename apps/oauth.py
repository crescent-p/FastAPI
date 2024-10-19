from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from apps import models, schemas
from apps.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "c57893382b253d4d67f3288a6e78aa64712e0773a0c11dad4b5bd5e4dbbac95d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(datetime.now())
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
 

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't verify token")

    token = verify_access_token(token, credential_exception=credential_exception)

    user = db.query(models.Users).where(models.Users.id == token.id).first()

    return user