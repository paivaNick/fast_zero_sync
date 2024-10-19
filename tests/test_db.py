from sqlalchemy import create_engine, select

from fast_zero.models import User, table_registry

from dataclasses import asdict


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='nick', password='secret', email='teste@test')
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'nick'))

    assert asdict(user) == {
        'id': 1,
        'username': 'nick',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
    }
