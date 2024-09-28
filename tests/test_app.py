from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


# triple A
def test_read_root_return_ok_ola_mundo():
    # arrange
    client = TestClient(app)
    # act
    response = client.get('/')
    # asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ola, mundo!'}


def test_ola_html_return_ok_ola():
    client = TestClient(app)

    response = client.get('/ola')
    assert response.status_code == HTTPStatus.OK
    assert response.text == """<h1>ola, mundo! </h1>"""
