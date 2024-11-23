from http import HTTPStatus

from fast_zero.models import Todo, TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            '/todos/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'test todo',
                'description': 'test todo description',
                'state': 'draft',
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'id': 1,
            'title': 'test todo',
            'description': 'test todo description',
            'state': 'draft',
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(3, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_description_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='comer')
    )
    session.commit()

    response = client.get(
        '/todos/?description=comer',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='test todo',
            description='combined description',
            state=TodoState.todo,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='other title',
            description='other description',
            state=TodoState.todo,
        )
    )

    session.commit()

    response = client.get(
        '/todos/?title=test todo&description=combined description&state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'task has been deleted successfully'}


def test_delete_todo_not_exists(client, token):
    response = client.delete(
        f'/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_update_todo(client, session, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste'


def test_patch_update_todo_not_exists(client, token):
    response = client.patch(
        f'/todos/{10}',
        json={'title': 'erro'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}