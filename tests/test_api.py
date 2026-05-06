"""
Backend tests for Mergington High School API using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        Arrange: No setup needed, activities are pre-loaded.
        Act: Send GET request to /activities.
        Assert: Verify response status and that activities are returned.
        """
        # Arrange
        expected_activity_names = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club",
        }

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert set(activities.keys()) == expected_activity_names
        for activity_name, details in activities.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_existing_activity_successfully(self, client):
        """
        Test successful signup for an existing activity.
        
        Arrange: Define a valid activity and email.
        Act: Send POST request to signup.
        Assert: Verify response status and success message.
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """
        Test signup for a non-existent activity returns 404.
        
        Arrange: Define a non-existent activity.
        Act: Send POST request to signup.
        Assert: Verify 404 status and error message.
        """
        # Arrange
        activity_name = "Non Existent Club"
        email = "user@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_duplicate_signup_returns_400(self, client):
        """
        Test that signing up the same email twice returns 400.
        
        Arrange: Sign up a user for an activity.
        Act: Attempt to sign up the same user again for the same activity.
        Assert: Verify 400 status and duplicate error message.
        """
        # Arrange
        activity_name = "Programming Class"
        email = "duplicate@mergington.edu"

        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert response1.status_code == 200

        # Act
        # Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Student already signed up"


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_participant_successfully(self, client):
        """
        Test successful removal of a participant from an activity.
        
        Arrange: Sign up a user for an activity.
        Act: Send DELETE request to remove the participant.
        Assert: Verify response status and success message.
        """
        # Arrange
        activity_name = "Art Club"
        email = "artist@mergington.edu"

        # Sign up first
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    def test_unregister_nonexistent_participant_returns_404(self, client):
        """
        Test unregistering a non-existent participant returns 404.
        
        Arrange: Define a participant that is not signed up.
        Act: Send DELETE request for the non-existent participant.
        Assert: Verify 404 status and error message.
        """
        # Arrange
        activity_name = "Drama Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """
        Test unregistering from a non-existent activity returns 404.
        
        Arrange: Define a non-existent activity.
        Act: Send DELETE request for the non-existent activity.
        Assert: Verify 404 status and error message.
        """
        # Arrange
        activity_name = "Non Existent Club"
        email = "user@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
