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
class ConfigModel(BaseModel):
    Monitoring_status: bool | None = None
    streaming_URL: str | None = None
    email: str

class ResultModel(BaseModel):
    username: str | None = None
    DATE_TIME: datetime | None = None
    config: str 
    result: int | None = None
    processed_detection_image: str
    

db_dependency = Annotated[Session, Depends(get_db)]

# Create a user using the variables
@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: ConfigModel, db: db_dependency):
    # Create a new user using the variables
    db_user = models.Config(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get the generated ID and other fields
    
    return db_user

# Create a data using the variables
@app.post("/create-data", status_code=status.HTTP_201_CREATED)
def create_data(data: ResultModel, db: db_dependency):
    # Create a new user using the variables
    db_data = models.Result(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)  # Refresh to get the generated ID and other fields
    
    return db_data

from fastapi import HTTPException

@app.delete("/delete-data/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_by_result_id(result_id: int, db: db_dependency):
    # Find the data entry by result_id
    db_data = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    # Delete the data entry
    db.delete(db_data)
    db.commit()
    return {"message": "Data deleted successfully"}

@app.delete("/delete-data-by-user/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_by_username(username: int, db: db_dependency):
    # Find all data entries by username
    db_data = db.query(models.Result).filter(models.Result.username == username)
    
    # Check if any data entries exist for the provided username
    if db_data.count() == 0:
        raise HTTPException(status_code=404, detail="No data found for this user")

    # Delete all data entries for the specified username
    db_data.delete(synchronize_session=False)
    db.commit()
    return {"message": "Data entries deleted successfully"}

@app.delete("/delete-user/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: int, db: db_dependency):
    # Check if there are any data entries for this user
    data_entries = db.query(models.Result).filter(models.Result.username == username).all()
    
    # If there are data entries, return a message
    if data_entries:
        raise HTTPException(
            status_code=400,
            detail="User has associated data entries. Please call the 'delete_data_by_userid' endpoint first."
        )
    
    # Find the user by username
    user = db.query(models.Config).filter(models.Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

from fastapi import HTTPException

@app.get("/get-user/{username}", response_model=ConfigModel)
def get_user_by_username(username: int, db: db_dependency):
    user = db.query(models.Config).filter(models.Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/get-data/{result_id}", response_model=ResultModel)
def get_data_by_result_id(result_id: int, db: db_dependency):
    data_entry = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    if not data_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return data_entry

@app.get("/get-last-24-data", response_model=List[ResultModel])
def get_last_24_data(db: db_dependency):
    data_entries = (
        db.query(models.Result)
        .order_by(models.Result.datetime.desc())
        .limit(24)
        .all()
    )
    return data_entries

@app.put("/update-user/{username}", response_model=ConfigModel)
def update_user(username: int, user_update: ConfigModel, db: db_dependency):
    user = db.query(models.Config).filter(models.Config.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.put("/update-data/{result_id}", response_model=ResultModel)
def update_data(result_id: int, data_update: ResultModel, db: db_dependency):
    data_entry = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    if not data_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    # Update fields if provided
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(data_entry, key, value)
    
    db.commit()
    db.refresh(data_entry)
    return data_entry