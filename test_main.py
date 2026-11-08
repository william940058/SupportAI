from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order_invalid_amount():
    response = client.post(
        "/orders",
        json={
            "user_id": 1,
            "product_name": "Gaming Mouse",
            "total_amount": -10
        }
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "user_id, product_name, total_amount",
    [
        (0, "Gaming Mouse", 59.99),
        (1, "", 59.99),
        (1, "Gaming Mouse", -10),
        (1, "Gaming Mouse", 0),
    ]
)
def test_create_order_invalid_inputs(
    user_id,
    product_name,
    total_amount
):
    response = client.post(
        "/orders",
        json={
            "user_id": user_id,
            "product_name": product_name,
            "total_amount": total_amount
        }
    )

    assert response.status_code == 422


def test_get_order_with_mock():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = (
        1,
        1,
        "Mechanical Keyboard",
        "shipped",
        129.99
    )

    fake_connection = MagicMock()
    fake_connection.__enter__.return_value = fake_connection
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor

    with patch("main.get_connection", return_value=fake_connection):
        response = client.get("/orders/1")

    assert response.status_code == 200
    assert response.json() == {
        "order_id": 1,
        "user_id": 1,
        "product_name": "Mechanical Keyboard",
        "status": "shipped",
        "total_amount": 129.99
    }

    fake_cursor.execute.assert_called_once()


def test_get_order_not_found():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = None

    fake_connection = MagicMock()
    fake_connection.__enter__.return_value = fake_connection
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor

    with patch("main.get_connection", return_value=fake_connection):
        response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }

    fake_cursor.execute.assert_called_once()


def test_create_order_with_mock():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = (
        2,
        1,
        "Gaming Mouse",
        "pending",
        59.99
    )

    fake_connection = MagicMock()
    fake_connection.__enter__.return_value = fake_connection
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor

    with patch("main.get_connection", return_value=fake_connection):
        response = client.post(
            "/orders",
            json={
                "user_id": 1,
                "product_name": "Gaming Mouse",
                "total_amount": 59.99
            }
        )

    assert response.status_code == 201
    assert response.json() == {
        "order_id": 2,
        "user_id": 1,
        "product_name": "Gaming Mouse",
        "status": "pending",
        "total_amount": 59.99
    }

    fake_cursor.execute.assert_called_once()


