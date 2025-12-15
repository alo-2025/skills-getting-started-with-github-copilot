import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Fixture to reset activities before each test
@pytest.fixture(autouse=True)
def reset_activities():
    # Reset to original state
    original_activities = {
        "Chess Club": {
            "category": "Intellectual",
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "category": "Intellectual",
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Debate Club": {
            "category": "Intellectual",
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Science Olympiad": {
            "category": "Intellectual",
            "description": "Compete in science competitions and conduct experiments",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["james@mergington.edu", "sarah@mergington.edu"]
        },
        "Gym Class": {
            "category": "Sports",
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "category": "Sports",
            "description": "Join the varsity and intramural basketball teams",
            "schedule": "Tuesdays, Thursdays, Saturdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["marcus@mergington.edu", "jessica@mergington.edu"]
        },
        "Track and Field": {
            "category": "Sports",
            "description": "Train for sprints, distance, and field events",
            "schedule": "Mondays through Fridays, 3:45 PM - 5:00 PM",
            "max_participants": 40,
            "participants": ["ryan@mergington.edu"]
        },
        "Drama Club": {
            "category": "Artistic",
            "description": "Perform in school plays and theatrical productions",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Art Workshop": {
            "category": "Artistic",
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["madison@mergington.edu"]
        },
        "Music Band": {
            "category": "Artistic",
            "description": "Play instruments and perform in concerts",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 22,
            "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
        }
    }
    activities.clear()
    activities.update(original_activities)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]
    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_unregister_success():
    response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]
    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/unregister?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"