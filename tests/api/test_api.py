"""tests/api/test_api.py — API tests: GET, POST, PUT, DELETE, parametrized."""

import pytest
from playwright.sync_api import APIRequestContext, Playwright


@pytest.fixture(scope="module")
def api(playwright: Playwright, api_base_url: str) -> APIRequestContext:
    request_context = playwright.request.new_context(base_url=api_base_url)
    yield request_context
    request_context.dispose()


@pytest.mark.smoke
@pytest.mark.api
def test_get_all_posts(api: APIRequestContext):
    response = api.get("/posts")
    assert response.status == 200
    assert len(response.json()) == 100


@pytest.mark.smoke
@pytest.mark.api
def test_get_single_post(api: APIRequestContext):
    response = api.get("/posts/1")
    assert response.status == 200
    post = response.json()
    assert {"id", "userId", "title", "body"}.issubset(post.keys())
    assert post["id"] == 1


@pytest.mark.api
def test_get_post_not_found(api: APIRequestContext):
    assert api.get("/posts/9999").status == 404


@pytest.mark.api
def test_get_comments_for_post(api: APIRequestContext):
    response = api.get("/posts/1/comments")
    assert response.status == 200
    comments = response.json()
    assert len(comments) > 0
    for comment in comments:
        assert comment["postId"] == 1


@pytest.mark.smoke
@pytest.mark.api
def test_create_post(api: APIRequestContext):
    payload  = {"title": "ShopTest Pro", "body": "Playwright API Test", "userId": 1}
    response = api.post("/posts", data=payload)
    assert response.status == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert "id" in created


@pytest.mark.api
def test_update_post(api: APIRequestContext):
    payload  = {"id": 1, "title": "Updated title", "body": "Updated body", "userId": 1}
    response = api.put("/posts/1", data=payload)
    assert response.status == 200
    assert response.json()["title"] == "Updated title"


@pytest.mark.api
def test_delete_post(api: APIRequestContext):
    assert api.delete("/posts/1").status == 200


@pytest.mark.api
def test_get_users(api: APIRequestContext):
    response = api.get("/users")
    assert response.status == 200
    users = response.json()
    assert len(users) == 10
    for user in users:
        assert "@" in user.get("email", "")


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
def test_get_multiple_posts_parametrized(api: APIRequestContext, post_id: int):
    response = api.get(f"/posts/{post_id}")
    assert response.status == 200
    assert response.json()["id"] == post_id
