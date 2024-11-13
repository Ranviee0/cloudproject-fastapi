from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for the request body
class UserModel(BaseModel):
    status: str | None = None
    url: str
    resultid: str

class DataModel(BaseModel):
    datetime: datetime
    config: str | None = None
    result: int
    image: str
    userid: int

db_dependency = Annotated[Session, Depends(get_db)]

# Create a user using the variables
@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserModel, db: db_dependency):
    # Create a new user using the variables
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get the generated ID and other fields
    
    return db_user

# Create a data using the variables
@app.post("/create-data", status_code=status.HTTP_201_CREATED)
def create_data(data: DataModel, db: db_dependency):
    # Create a new user using the variables
    db_data = models.Data(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)  # Refresh to get the generated ID and other fields
    
    return db_data

from fastapi import HTTPException

@app.delete("/delete-data/{resultid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_by_resultid(resultid: int, db: db_dependency):
    # Find the data entry by resultid
    db_data = db.query(models.Data).filter(models.Data.resultid == resultid).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    # Delete the data entry
    db.delete(db_data)
    db.commit()
    return {"message": "Data deleted successfully"}

@app.delete("/delete-data-by-user/{userid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_by_userid(userid: int, db: db_dependency):
    # Find all data entries by userid
    db_data = db.query(models.Data).filter(models.Data.userid == userid)
    
    # Check if any data entries exist for the provided userid
    if db_data.count() == 0:
        raise HTTPException(status_code=404, detail="No data found for this user")

    # Delete all data entries for the specified userid
    db_data.delete(synchronize_session=False)
    db.commit()
    return {"message": "Data entries deleted successfully"}

@app.delete("/delete-user/{userid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(userid: int, db: db_dependency):
    # Check if there are any data entries for this user
    data_entries = db.query(models.Data).filter(models.Data.userid == userid).all()
    
    # If there are data entries, return a message
    if data_entries:
        raise HTTPException(
            status_code=400,
            detail="User has associated data entries. Please call the 'delete_data_by_userid' endpoint first."
        )
    
    # Find the user by userid
    user = db.query(models.User).filter(models.User.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

from fastapi import HTTPException

@app.get("/get-user/{userid}", response_model=UserModel)
def get_user_by_userid(userid: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/get-data/{resultid}", response_model=DataModel)
def get_data_by_resultid(resultid: int, db: db_dependency):
    data_entry = db.query(models.Data).filter(models.Data.resultid == resultid).first()
    if not data_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return data_entry

@app.get("/get-last-24-data", response_model=List[DataModel])
def get_last_24_data(db: db_dependency):
    data_entries = (
        db.query(models.Data)
        .order_by(models.Data.datetime.desc())
        .limit(24)
        .all()
    )
    return data_entries

@app.put("/update-user/{userid}", response_model=UserModel)
def update_user(userid: int, user_update: UserModel, db: db_dependency):
    user = db.query(models.User).filter(models.User.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.put("/update-data/{resultid}", response_model=DataModel)
def update_data(resultid: int, data_update: DataModel, db: db_dependency):
    data_entry = db.query(models.Data).filter(models.Data.resultid == resultid).first()
    if not data_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    # Update fields if provided
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(data_entry, key, value)
    
    db.commit()
    db.refresh(data_entry)
    return data_entry