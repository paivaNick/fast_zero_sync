from http import HTTPStatus

# triple A


def test_read_root_return_ok_ola_mundo(client):
    # arrange
    # act
    response = client.get('/')
    # asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'olá, mundo!'}
