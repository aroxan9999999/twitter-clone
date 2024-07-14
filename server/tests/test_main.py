import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from server.app.main import app, get_db
from server.app import models, crud
from server.app.database import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup():
    db = TestingSessionLocal()
    db.query(models.User).delete()
    db.query(models.Tweet).delete()
    db.query(models.Follow).delete()
    db.query(models.Like).delete()
    db.query(models.Media).delete()
    db.commit()

    # Добавление тестовых данных
    user1 = models.User(id=1, name="User 1", api_key="key1")
    user2 = models.User(id=2, name="User 2", api_key="key2")
    db.add(user1)
    db.add(user2)
    db.commit()
    db.close()

    yield

def test_create_tweet(setup):
    response = client.post(
        "/api/tweets",
        json={"content": "Hello World!", "media_ids": []},
        headers={"api-key": "key1"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True
    assert "tweet_id" in response.json()

def test_like_tweet(setup):
    response = client.post(
        "/api/tweets",
        json={"content": "Hello Again!", "media_ids": []},
        headers={"api-key": "key1"}
    )
    tweet_id = response.json()["tweet_id"]

    response = client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "key2"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True

def test_follow_user(setup):
    response = client.post(
        "/api/users/2/follow",
        headers={"api-key": "key1"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True

def test_get_feed(setup):
    response = client.get(
        "/api/tweets",
        headers={"api-key": "key1"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == True
    assert "tweets" in response.json()
