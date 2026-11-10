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

def test_search_knowledge():
    response = client.get(
        "knowledge/search",
        params={"keyword": "refund"}
    )
    
    assert response.status_code == 200

    data = response.json()

    assert data["keyword"] == "refund"
    assert data["count"] == 3
    assert len(data["results"]) == 3

def test_search_knowledge_no_results():
    response = client.get(
        "knowledge/search",
        params={"keyword": "warranty"}
    )
    
    assert response.status_code == 200

    data = response.json()

    assert data["keyword"] == "warranty"
    assert data["count"] == 0
    assert data["results"] == []

def test_search_knowledge_missing_keyword():
    response = client.get("knowledge/search")
    
    assert response.status_code == 422

##
def test_semantic_knowledge():
    response = client.get(
        "knowledge/semantic-search",
        params={"query": "How long does it take to receive my refund?"}
    )
    
    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "How long does it take to receive my refund?"
    assert "5-7 business days" in data["best_match"]
    assert isinstance(data["similarity"], float)

def test_semantic_search_with_mock():
    fake_result = {
        "question": "refund",
        "best_match": "Refunds take 5-7 business days.",
        "similarity": 0.95
    }

    with patch("main.semantic_search", return_value=fake_result):
        response = client.get(
            "/knowledge/semantic-search",
            params={"query": "refund"}
        )

    assert response.status_code == 200
    assert response.json() == fake_result
