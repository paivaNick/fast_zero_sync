from fastapi import FastAPI
from schemas import UserSchema


app = FastAPI()


database = []


@app.get('/')
def read_root():
    return {'message': 'main page'}


@app.get('/users/')
def create_user(user: UserSchema):
    user_with_id = UserDB
