def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "not.signed.up@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": missing_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_unregister_matches_email_case_insensitively_and_with_spaces(client):
    # Arrange
    activity_name = "Basketball Team"
    email_with_spaces_and_case = "  ALEX@MERGINGTON.EDU  "

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email_with_spaces_and_case},
    )
    payload = response.json()
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == "Unregistered alex@mergington.edu from Basketball Team"
    assert "alex@mergington.edu" not in activities[activity_name]["participants"]
