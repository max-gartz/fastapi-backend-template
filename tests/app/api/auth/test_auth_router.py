from tests.init_main import client


def test_login_not_found() -> None:
    response = client.post(
        "/auth/login",
        json={"email": "test.user@email.com", "password": "password"}
    )
    assert response.status_code == 404
