from http import HTTPStatus

from src.app import Role, User, db


def test_login_success(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="john-doe",
        password="testing",
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": user.username,
            "password": user.password,
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_login_fail(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="john-doe",
        password="testing",
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": user.username,
            "password": "",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {
        "msg": "Wrong name or password. Try again.",
    }
