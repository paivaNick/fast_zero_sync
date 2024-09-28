from fastapi import FastAPI
from http import HTTPStatus
from fastapi.responses import HTMLResponse
from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'ola, mundo!'}


@app.get('/message', status_code=HTTPStatus.OK, response_model=Message)
def message():
    return {'message': 'oi'}


@app.get('/ola', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def ola_html():
    return """<h1>ola, mundo! </h1>"""
