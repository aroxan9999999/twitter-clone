
# Twitter Clone API

This is a Twitter clone API built using FastAPI. The API supports various functionalities such as creating tweets, deleting tweets, following/unfollowing users, liking/unliking tweets, and more.

## Functional Requirements

1. Users can add a new tweet.
2. Users can delete their own tweet.
3. Users can follow another user.
4. Users can unfollow another user.
5. Users can like a tweet.
6. Users can unlike a tweet.
7. Users can get a feed of tweets sorted by popularity from users they follow.
8. Tweets can contain an image.

Note: User registration is not required. Users will be created by the corporate network.

## Non-functional Requirements

1. The system should be easy to deploy using Docker Compose.
2. The system should not lose user data between runs.
3. All service responses should be documented using Swagger. Documentation should be available at application startup.
4. Provide a detailed README with project description and instructions for running the application.

## Endpoints

### 1. Create a new tweet
**POST /api/tweets**

**Request Headers:**
- api-key: str

**Request Body:**
```json
{
    "tweet_data": "string",
    "tweet_media_ids": [1, 2] // Optional
}
```

**Response:**
```json
{
    "result": true,
    "tweet_id": int
}
```

### 2. Upload media file

**POST /api/medias**

**Request Headers:**
- api-key: str

**Request Form:**
- file: "image.jpg"

**Response:**
```json
{
    "result": true,
    "media_id": int
}
```

### 3. Delete a tweet

**DELETE /api/tweets/{id}**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true
}
```

### 4. Like a tweet

**POST /api/tweets/{id}/likes**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true
}
```

### 5. Unlike a tweet

**DELETE /api/tweets/{id}/likes**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true
}
```

### 6. Follow a user

**POST /api/users/{id}/follow**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true
}
```

### 7. Unfollow a user

**DELETE /api/users/{id}/follow**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true
}
```

### 8. Get user's feed

**GET /api/tweets**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true,
    "tweets": [
        {
            "id": int,
            "content": string,
            "attachments": [
                "link_1",
                "link_2"
            ],
            "author": {
                "id": int,
                "name": string
            },
            "likes": [
                {
                    "user_id": int,
                    "name": string
                }
            ]
        },
        ...
    ]
}
```

### 9. Get user's profile

**GET /api/users/me**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true,
    "user": {
        "id": int,
        "name": string,
        "followers": [
            {
                "id": int,
                "name": string
            }
        ],
        "following": [
            {
                "id": int,
                "name": string
            }
        ]
    }
}
```

### 10. Get another user's profile by ID

**GET /api/users/{id}**

**Request Headers:**
- api-key: str

**Response:**
```json
{
    "result": true,
    "user": {
        "id": int,
        "name": string,
        "followers": [
            {
                "id": int,
                "name": string
            }
        ],
        "following": [
            {
                "id": int,
                "name": string
            }
        ]
    }
}
```

## Running the Project
### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

```bash
git clone <repository_url>
cd twitter-clone
```

2. Create a .env file in the root directory of the project and add your database URL:

```bash
DATABASE_URL=postgresql://user:password@db:5432/twitter_clone
```

3. Build and start the containers:

```bash
docker-compose up -d
```

4. Access the API documentation at [http://localhost:5000/docs](http://localhost:5000/docs)

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

## Project Structure

- `app/main.py`: The main FastAPI application.
- `app/models.py`: The SQLAlchemy models.
- `app/schemas.py`: The Pydantic schemas.
- `app/crud.py`: The CRUD operations.
- `app/database.py`: The database setup.
- `tests/`: The test files.

