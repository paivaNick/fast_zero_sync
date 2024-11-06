from http import HTTPStatus


def get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['type'] == 'Bearer'
    assert 'access_token' in token
