def test_create_product(client):
    response = client.post(
        "/admin/products/",
        json={"name": "Test Product", "description": "Desc", "price": 10.0, "stock": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert "id" in data

def test_read_products_admin(client):
    response = client.get("/admin/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_product(client):
    # First create
    resp1 = client.post(
        "/admin/products/",
        json={"name": "Update Me", "price": 20.0, "stock": 10}
    )
    product_id = resp1.json()["id"]

    # Now update
    resp2 = client.put(
        f"/admin/products/{product_id}",
        json={"price": 25.0}
    )
    assert resp2.status_code == 200
    assert resp2.json()["price"] == 25.0
    assert resp2.json()["name"] == "Update Me"

def test_delete_product(client):
    resp = client.post(
        "/admin/products/",
        json={"name": "Delete Me", "price": 10.0, "stock": 5}
    )
    product_id = resp.json()["id"]

    del_resp = client.delete(f"/admin/products/{product_id}")
    assert del_resp.status_code == 200

    # Ensure it's deleted
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404

def test_admin_orders(client):
    # Get all orders
    resp = client.get("/admin/orders/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_admin_update_order_status(client):
    # Need to create an order first
    # 1. create product
    prod_resp = client.post(
        "/admin/products/",
        json={"name": "Order Status Product", "price": 100.0, "stock": 10}
    )
    product_id = prod_resp.json()["id"]

    # 2. place order
    order_resp = client.post(
        "/checkout/",
        json={
            "customer_name": "Test User",
            "customer_email": "test@test.com",
            "items": [{"product_id": product_id, "quantity": 1}]
        }
    )
    order_id = order_resp.json()["id"]

    # 3. update status
    update_resp = client.put(f"/admin/orders/{order_id}/status?status=completed")
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"
