def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"QuickOrder" in response.data


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_restaurants_api_requires_key(client):
    assert client.get("/api/restaurants").status_code == 401
    response = client.get("/api/restaurants", headers={"X-API-Key": "quickorder-demo-key"})
    assert response.status_code == 200
    assert response.get_json()["count"] == 1


def test_swagger_and_openapi(client):
    assert client.get("/docs/").status_code == 200
    assert client.get("/openapi.yaml").status_code == 200


def test_login_and_profile(client):
    response = client.post("/login", data={"email": "test@example.com", "password": "Password123!"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Mon profil" in response.data


def test_api_orders_with_key(client):
    response = client.get("/api/orders", headers={"X-API-Key": "quickorder-demo-key"})
    assert response.status_code == 200
