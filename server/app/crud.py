from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_api_key(db: Session, api_key: str):
    print(f"Querying user with API key: {api_key}")  # Отладочное сообщение
    return db.query(models.User).filter(models.User.api_key == api_key).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, api_key=user.api_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.api_key = user.api_key
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def create_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    db_tweet = models.Tweet(content=tweet.content, author_id=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    for media_id in tweet.media_ids:
        db_media = db.query(models.Media).filter(models.Media.id == media_id).first()
        if db_media:
            db_tweet.media.append(db_media)
    db.commit()
    return db_tweet

def delete_tweet(db: Session, tweet_id: int, user_id: int):
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id, models.Tweet.author_id == user_id).first()
    if db_tweet:
        db.delete(db_tweet)
        db.commit()
    return db_tweet

def follow_user(db: Session, follower_id: int, followed_id: int):
    db_follow = models.Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(db_follow)
    db.commit()
    return db_follow

def unfollow_user(db: Session, follower_id: int, followed_id: int):
    db_follow = db.query(models.Follow).filter(models.Follow.follower_id == follower_id, models.Follow.followed_id == followed_id).first()
    if db_follow:
        db.delete(db_follow)
        db.commit()
    return db_follow

def like_tweet(db: Session, user_id: int, tweet_id: int):
    db_like = models.Like(user_id=user_id, tweet_id=tweet_id)
    db.add(db_like)
    db.commit()
    return db_like

def unlike_tweet(db: Session, user_id: int, tweet_id: int):
    db_like = db.query(models.Like).filter(models.Like.user_id == user_id, models.Like.tweet_id == tweet_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like

def get_feed(db: Session, user_id: int):
    follows = db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()
    followed_ids = [follow.followed_id for follow in follows]
    tweets = db.query(models.Tweet).filter(models.Tweet.author_id.in_(followed_ids)).order_by(models.Tweet.id.desc()).all()
    return tweets
