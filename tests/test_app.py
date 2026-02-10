"""Tests for the FastAPI application endpoints"""
import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that get activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_has_correct_structure(self, client):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        # Check Chess Club structure
        chess = data["Chess Club"]
        assert "description" in chess
        assert "schedule" in chess
        assert "max_participants" in chess
        assert "participants" in chess
        assert isinstance(chess["participants"], list)
        assert chess["max_participants"] == 12

    def test_get_activities_includes_participants(self, client):
        """Test that activities include participant lists"""
        response = client.get("/activities")
        data = response.json()
        
        chess = data["Chess Club"]
        assert "michael@mergington.edu" in chess["participants"]
        assert "daniel@mergington.edu" in chess["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        email = "newstudent@mergington.edu"
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for Chess Club"
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for an activity that doesn't exist"""
        email = "student@mergington.edu"
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": email}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student(self, client):
        """Test that a student cannot sign up twice for the same activity"""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_multiple_activities(self, client):
        """Test that a student can sign up for multiple different activities"""
        email = "versatile@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_signup_with_special_characters_in_name(self, client):
        """Test signup for activities with special characters"""
        email = "student@mergington.edu"
        response = client.post(
            "/activities/Math Olympiad/signup",
            params={"email": email}
        )
        assert response.status_code == 200


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity"""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from Chess Club"
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregister from an activity that doesn't exist"""
        email = "student@mergington.edu"
        response = client.delete(
            "/activities/Nonexistent Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_signed_up(self, client):
        """Test unregister when student is not signed up for the activity"""
        email = "notsignedug@mergington.edu"
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_signup_then_unregister(self, client):
        """Test signing up and then unregistering from an activity"""
        email = "temporary@mergington.edu"
        
        # First, sign up
        signup_response = client.post(
            "/activities/Art Studio/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signed up
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Art Studio"]["participants"]
        
        # Now unregister
        unregister_response = client.delete(
            "/activities/Art Studio/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Art Studio"]["participants"]

    def test_unregister_does_not_affect_other_participants(self, client):
        """Test that unregistering one student doesn't affect others"""
        email = "daniel@mergington.edu"  # Already in Chess Club
        other_email = "michael@mergington.edu"  # Also in Chess Club
        
        # Get initial count
        activities_response = client.get("/activities")
        initial_count = len(activities_response.json()["Chess Club"]["participants"])
        
        # Unregister one student
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify other student is still there
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Chess Club"]["participants"]
        assert other_email in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == initial_count - 1


class TestIntegration:
    """Integration tests for the application"""

    def test_full_workflow(self, client):
        """Test a complete workflow: view activities, sign up, verify, unregister"""
        email = "integration@mergington.edu"
        activity = "Soccer Club"
        
        # 1. View all activities
        response = client.get("/activities")
        assert response.status_code == 200
        initial_participants = response.json()[activity]["participants"]
        assert email not in initial_participants
        
        # 2. Sign up for an activity
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # 3. Verify signup
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # 4. Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # 5. Verify unregistration
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_concurrent_signups_different_activities(self, client):
        """Test signing up for multiple activities"""
        email = "multitasker@mergington.edu"
        activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all signups
        response = client.get("/activities")
        all_activities = response.json()
        for activity in activities:
            assert email in all_activities[activity]["participants"]
