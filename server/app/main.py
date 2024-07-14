from fastapi import FastAPI, HTTPException, Depends, Header, File, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Twitter Clone API",
    description="API for a Twitter clone application. Allows users to create tweets, like/unlike tweets, follow/unfollow users, and more.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(api_key: str = Header(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_api_key(db, api_key)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"result": True, "user": current_user}

@app.post("/api/tweets", response_model=schemas.Tweet)
def create_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_tweet = crud.create_tweet(db, tweet, current_user.id)
    return {"result": True, "tweet_id": db_tweet.id}

@app.delete("/api/tweets/{tweet_id}", response_model=schemas.OperationResult)
def delete_tweet(tweet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.delete_tweet(db, tweet_id, current_user.id)
    return {"result": True}

@app.post("/api/users/{user_id}/follow", response_model=schemas.OperationResult)
def follow_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    follow = crud.follow_user(db, current_user.id, user_id)
    return {"result": True, "follow": follow}

@app.delete("/api/users/{user_id}/follow", response_model=schemas.OperationResult)
def unfollow_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    unfollow = crud.unfollow_user(db, current_user.id, user_id)
    return {"result": True, "unfollow": unfollow}

@app.post("/api/tweets/{tweet_id}/likes", response_model=schemas.OperationResult)
def like_tweet(tweet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.like_tweet(db, current_user.id, tweet_id)
    return {"result": True}

@app.delete("/api/tweets/{tweet_id}/likes", response_model=schemas.OperationResult)
def unlike_tweet(tweet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.unlike_tweet(db, current_user.id, tweet_id)
    return {"result": True}

@app.get("/api/tweets", response_model=schemas.Feed)
def get_feed(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tweets = crud.get_feed(db, current_user.id)
    return {"result": True, "tweets": tweets}

@app.post("/api/medias", response_model=schemas.MediaResponse)
def upload_media(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    file_location = f"media/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    db_media = models.Media(file_path=file_location)
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return {"result": True, "media_id": db_media.id}

@app.get("/api/users/{user_id}", response_model=schemas.UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.get_user(db, user_id)
    if not user:
        return JSONResponse(status_code=404, content={"result": False, "error_type": "UserNotFound", "error_message": "User not found"})
    followers = [{"id": follower.follower.id, "name": follower.follower.name} for follower in user.followers]
    following = [{"id": follow.followed.id, "name": follow.followed.name} for follow in user.following]
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": followers,
            "following": following
        }
    }
