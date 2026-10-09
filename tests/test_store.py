def test_read_products_store(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_checkout_success(client):
    # Create product for checkout
    prod_resp = client.post(
        "/admin/products/",
        json={"name": "Checkout Product", "description": "Checkout", "price": 100.0, "stock": 10}
    )
    product_id = prod_resp.json()["id"]

    # Place order
    response = client.post(
        "/checkout/",
        json={
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "items": [{"product_id": product_id, "quantity": 3}]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_price"] == 300.0
    assert data["status"] == "pending"
    
    # Verify stock is reduced
    get_prod = client.get(f"/products/{product_id}")
    assert get_prod.json()["stock"] == 7

def test_checkout_insufficient_stock(client):
    prod_resp = client.post(
        "/admin/products/",
        json={"name": "Low Stock Product", "price": 10.0, "stock": 2}
    )
    product_id = prod_resp.json()["id"]

    response = client.post(
        "/checkout/",
        json={
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "items": [{"product_id": product_id, "quantity": 5}]
        }
    )
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]

def test_get_order(client):
    # 1. create product
    prod_resp = client.post(
        "/admin/products/",
        json={"name": "Get Order Product", "price": 50.0, "stock": 10}
    )
    product_id = prod_resp.json()["id"]

    # 2. place order
    order_resp = client.post(
        "/checkout/",
        json={
            "customer_name": "Retrieve User",
            "customer_email": "retrieve@example.com",
            "items": [{"product_id": product_id, "quantity": 1}]
        }
    )
    order_id = order_resp.json()["id"]

    # 3. get order
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["customer_name"] == "Retrieve User"
    assert data["total_price"] == 50.0
