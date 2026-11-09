from knowledge import search_knowledge
from database import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI(title="SupportAI API")


class ChatRequest(BaseModel):
    message: str

class OrderCreate(BaseModel):
    user_id: int = Field(gt=0)
    product_name: str = Field(min_length=1, max_length=200)
    total_amount: float = Field(gt=0)

class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "shipped", "delivered", "cancelled"]



@app.get("/")
def home():
    return {"message": "Welcome to SupportAI!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "reply": f"You said: {request.message}"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, user_id, product_name, status, total_amount
                FROM orders
                WHERE id = %s;
                """,
                (order_id,)
            )
            order = cur.fetchone()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order[0],
        "user_id": order[1],
        "product_name": order[2],
        "status": order[3],
        "total_amount": float(order[4])
    }


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO orders
                    (user_id, product_name, total_amount)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, product_name,
                          status, total_amount;
                """,
                (
                    order.user_id,
                    order.product_name,
                    order.total_amount
                )
            )
            new_order = cur.fetchone()

    return {
        "order_id": new_order[0],
        "user_id": new_order[1],
        "product_name": new_order[2],
        "status": new_order[3],
        "total_amount": float(new_order[4])
    }

@app.patch("/orders/{order_id}")
def update_order_status(order_id: int, update: OrderStatusUpdate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE orders
                SET status = %s
                WHERE id = %s
                RETURNING id, user_id, product_name,
                          status, total_amount;
                """,
                (update.status, order_id)
            )
            updated_order = cur.fetchone()

    if updated_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": updated_order[0],
        "user_id": updated_order[1],
        "product_name": updated_order[2],
        "status": updated_order[3],
        "total_amount": float(updated_order[4])
    }

@app.delete("/orders/{order_id}", status_code= 204)
def delete_order(order_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM orders
                WHERE id = %s
                RETURNING id
                """,
                (order_id,)
            )
            deleted_order = cur.fetchone()

    if deleted_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


@app.get("/knowledge/search")
def search_knowledge_endpoint(keyword: str):
    results = search_knowledge(keyword)

    return {
        "keyword": keyword,
        "results": results,
        "count": len(results)
    }
