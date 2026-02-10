"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture(scope="function")
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Team soccer practice and intramural matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Skills training and competitive games",
            "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "ella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops and stage productions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["henry@mergington.edu", "grace@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Problem solving and competition preparation",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["amelia@mergington.edu", "james@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and research projects",
            "schedule": "Fridays, 2:30 PM - 4:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        }
    })
