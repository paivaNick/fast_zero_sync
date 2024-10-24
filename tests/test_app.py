from http import HTTPStatus

from fast_zero.schemas import UserPublic

# triple A


def test_read_root_return_ok_ola_mundo(client):
    # arrange
    # act
    response = client.get('/')
    # asserts
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'olá, mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'username',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'username',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_should_return_400_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'romarinho@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_should_return_400_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'romarinho',
            'email': user.email,
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'test',
            'password': '123',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'user deleted!'}


def test_read_nonexistent_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}


def test_update_nonexistent_user(client):
    response = client.put(
        '/users/898',
        json={
            'username': 'test',
            'password': '123',
            'email': 'test@test.com',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}


def test_delete_nonexistent_user(client):
    response = client.delete(
        '/users/898',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}
