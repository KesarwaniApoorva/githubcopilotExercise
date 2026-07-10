from fastapi.testclient import TestClient

from src.app import app, activities


def test_signup_for_activity_adds_participant():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_duplicate_returns_bad_request():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_them():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_missing_participant_returns_not_found():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
