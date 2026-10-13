"""Backend tests for the Mergington High School API (Arrange-Act-Assert)."""
import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)
_ORIGINAL = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_ORIGINAL))
    yield


def test_get_activities_returns_all():
    # Arrange / Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_participant():
    # Arrange
    email = "new@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_rejected():
    # Arrange
    email = "michael@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity_404():
    response = client.post("/activities/Nope/signup", params={"email": "a@b.edu"})
    assert response.status_code == 404


def test_unregister_removes_participant():
    # Arrange
    email = "daniel@mergington.edu"
    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_400():
    response = client.delete("/activities/Chess Club/unregister", params={"email": "x@y.edu"})
    assert response.status_code == 400
