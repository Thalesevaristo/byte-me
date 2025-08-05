from http import HTTPStatus

from src.app import Role, User, Post, db


def test_get_post_success(client):
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

    post = Post(
        author_id=user.id,
        title="First Post",
        body="Hello World!",
    )
    db.session.add(post)
    db.session.commit()

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": post.id,
        "author_id": post.author_id,
        "title": post.title,
        "body": post.body,
    }


def test_get_user_fail(client):

    post_id = 1
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_post(client):
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
    token = response.json["access_token"]

    payload = {
        "title": "First Post",
        "body": "Hello World!",
        "author_id": user.id,
    }

    response = client.post(
        "/posts/",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Post created!"}


def test_list_posts(client):
    role = Role(name="user")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="john-doe",
        password="testing",
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    post = Post(
        title="First Post",
        body="Hello World!",
        author_id=user.id,
    )
    db.session.add(post)
    db.session.commit()

    response = client.get("/posts/")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "posts": [
            {
                "id": post.id,
                "title": post.title,
            }
        ]
    }
