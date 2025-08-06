from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models import db, User, Post
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint("post", __name__, url_prefix="/posts")


@jwt_required()
def create_post(data: dict) -> tuple[dict, int]:

    if not data or not data.get("title") or not data.get("body"):
        return {"msg": "Missing title or body"}, HTTPStatus.BAD_REQUEST

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user:
        return {"msg": "User not found"}, HTTPStatus.NOT_FOUND

    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=user.id,
    )
    db.session.add(post)
    db.session.commit()

    return {"msg": "User created!"}, HTTPStatus.CREATED


def list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    return [
        {
            "id": post.id,
            "title": post.title,
        }
        for post in posts
    ]


def get_post(post: Post) -> dict:

    return {
        "id": post.id,
        "author_id": post.author_id,
        "title": post.title,
        "body": post.body,
    }


def update_post(post: Post, data: dict) -> tuple[dict, int]:
    mapper = inspect(User)
    for column in mapper.attrs:
        key = column.key
        if key in data:
            setattr(post, key, data[key])
    db.session.commit()

    return get_post(post), HTTPStatus.OK


def delete_post(post: Post) -> tuple[str, int]:
    db.session.delete(post)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_post():

    if request.method == "POST":
        data = request.get_json()
        return create_post(data)

    else:
        return {"users": list_posts()}, HTTPStatus.OK


@app.route("/<int:post_id>", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
def post_control(post_id: int):
    post = db.get_or_404(Post, post_id)

    if request.method == "PATCH":
        data = request.get_json()
        return update_post(post, data)

    elif request.method == "DELETE":
        return delete_post(post)

    else:
        return get_post(post), HTTPStatus.OK
