import pytest
from unittest.mock import MagicMock
from app.controller.user_controller import (
    list_users_if_admin,
    check_user,
    add_user,
    get_user_by_id,
    update_user_info,
    delete_user,
)

def test_list_users_if_admin(mocker, mock_user):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.all.return_value = [mock_user]

    result = list_users_if_admin(0)  # Admin tier
    assert len(result) == 1
    assert result[0].email == "test@example.com"

    result = list_users_if_admin(1)  # Non-admin tier
    assert result == "Acceso denegado. Solo los administradores pueden listar usuarios."

def test_check_user(mocker, mock_user):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.filter_by.return_value.first.return_value = mock_user

    result = check_user("test@example.com", "password")
    assert result == mock_user

    mock_user.check_password.return_value = False
    result = check_user("test@example.com", "wrongpassword")
    assert result == ("Usuario o clave invalido", "danger")

def test_add_user(mocker, mock_db, mock_user):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.filter.return_value.first.return_value = None  # No user exists

    mock_user.set_password = MagicMock()
    mock_db.session.add = MagicMock()
    mock_db.session.commit = MagicMock()

    result = add_user(
        first_name="Test",
        last_name="User",
        dni="12345678",
        email="test@example.com",
        password="password",
        license_expiration="2025-01-01",
    )
    assert result == ("Usuario creado exitosamente!", "success")

def test_get_user_by_id(mocker, mock_user):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.get.return_value = mock_user

    result = get_user_by_id(1)
    assert result == mock_user

def test_update_user_info(mocker, mock_user, mock_db):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.get.return_value = mock_user

    result = update_user_info(
        user_id=1,
        first_name="Updated",
        email="updated@example.com",
    )
    assert result == ("Usuario actualizado con éxito", "success")
    assert mock_user.first_name == "Updated"
    assert mock_user.email == "updated@example.com"

def test_delete_user(mocker, mock_user, mock_db):
    mock_query = mocker.patch("app.model.user_model.User.query")
    mock_query.get.return_value = mock_user

    mock_db.session.delete = MagicMock()
    mock_db.session.commit = MagicMock()

    delete_user(1)
    mock_db.session.delete.assert_called_once_with(mock_user)
    mock_db.session.commit.assert_called_once()
