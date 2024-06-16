from ..routers.users import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "Heera"
    assert response.json()['email'] == "Heera@email.com"
    assert response.json()['first_name'] == "Heera"
    assert response.json()['last_name'] == "Singh"
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "7777777777"


def test_change_password_user(test_user):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrongpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    number = "7777777776"
    response = client.put(f"/user/phonenumber/{number}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert test_user.phone_number == number
