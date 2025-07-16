from fastapi import Depends, FastAPI, HTTPException
from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security.api_key import APIKeyHeader, APIKey
from sqlalchemy.orm import Session
import datetime
import sql_model
import crud
import schemas

sql_model.Base.metadata.create_all(bind=sql_model.engine)

app = FastAPI()

def get_db():
    db = sql_model.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/")
def create(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db, username = user.username)
    if db_user:
        raise HTTPException(status_code=401, detail="username already registered")
    return crud.create_user(db=db, user=user)


def read_keys():
    db1 = sql_model.SessionLocal()
    keys = crud.get_keys(db1)
    return keys
    

api_key_header = APIKeyHeader(name="api-key", auto_error=False)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    tokens = read_keys()
    if api_key_header in tokens:
        return api_key_header
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or missing API Key")


@app.get("/user/authenticate")
async def private(api_key: APIKey = Depends(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return {"default variable": api_key}

@app.get("/getUserData")
async def get_user(api_key: APIKey = Depends(get_api_key), db:Session=Depends(get_db)):
    db_user = crud.get_user_by_api(db, api_key = api_key)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exists")
    if db_user.expdate < datetime.datetime.utcnow():
        raise HTTPException(status_code=402, detail="Key expired")
    return db_user
