import pytest
from fastapi.testclient import TestClient
import src.app
import copy

@pytest.fixture(autouse=True)
def mock_activities(monkeypatch):
    # Arrange: Set up mock data for each test
    mock_data = {
        "Mock Club": {
            "description": "Mock description",
            "schedule": "Mondays, 1:00 PM - 2:00 PM",
            "max_participants": 5,
            "participants": ["test@mock.com"]
        }
    }
    monkeypatch.setattr(src.app, 'activities', copy.deepcopy(mock_data))
    yield
    # No teardown needed since data is in-memory and test-scoped

def test_get_activities():
    # Arrange
    client = TestClient(src.app.app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Mock Club" in data
    assert data["Mock Club"]["description"] == "Mock description"

def test_signup_for_activity_success():
    # Arrange
    client = TestClient(src.app.app)
    email = "newuser@mock.com"
    # Act
    response = client.post(f"/activities/Mock Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Mock Club"


def test_signup_for_activity_already_signed_up():
    # Arrange
    client = TestClient(src.app.app)
    email = "test@mock.com"
    # Act
    response = client.post(f"/activities/Mock Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
