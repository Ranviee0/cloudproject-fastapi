from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Result, Config

router = APIRouter()

@router.delete("/result/{username}")
def delete_results(username:str, db: Session = Depends(get_db)):
    results_to_delete = db.query(Result).filter(Result.username == username)
    if results_to_delete.count() == 0:
        raise HTTPException(status_code=404, detail=f"No results found for username '{username}'")
    
    results_to_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"All results for username '{username}' have been deleted."}

@router.delete("/config/{username}")
def delete_config(username:str, db: Session = Depends(get_db)):
    results_to_delete = db.query(Result).filter(Result.username == username)
    if results_to_delete.count() != 0:
        raise HTTPException(status_code=500, detail=f"Can't delete '{username}'")

    user_to_delete = db.query(Config).filter(Config.username == username)
    user_to_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"'{username}' was deleted."}

@router.delete("/twenty-four")
def twenty_four(db: Session = Depends(get_db)):
    print("H")
    # Query all users from the Config table
    configs = db.query(Config).all()
    
    if not configs:
        raise HTTPException(status_code=404, detail="No user data found.")

    for config in configs:
        username = config.username
        if not username:
            continue

        # Query to fetch all results for the user ordered by DATE_TIME
        user_results = db.query(Result).filter(Result.username == username).order_by(Result.DATE_TIME.desc()).all()

        # Keep only the latest 24 results, delete the rest
        if len(user_results) > 24:
            results_to_delete = user_results[24:]  # All results after the 24th
            for result in results_to_delete:
                db.delete(result)
    
    # Commit changes to the database
    db.commit()
    
    return {"detail": "Successfully retained the latest 24 results for each user."}