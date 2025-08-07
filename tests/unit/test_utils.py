from http import HTTPStatus
from utils.utils import requires_roles


def test_requires_roles_sucess(mocker):

    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = requires_roles("admin")(lambda: "OK")
    result = decorated_function()

    assert result == "OK"


def test_requires_roles_fail(mocker):

    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = requires_roles("admin")(lambda: "OK")
    result = decorated_function()

    assert result == ({"msg": "User don`t have acess level."}, HTTPStatus.FORBIDDEN)
