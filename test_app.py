from app import app 
# Import pytest for writing and running tests
import pytest

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200

def test_cibc_scenario(client):
    """Test the cibc scenario page."""
    response = client.get('/email-test')
    assert response.status_code == 200

def test_cibc_scenario_result(client):
    """Test the cibc scenario result."""
    response = client.get('/email-test/result')
    assert response.status_code == 200


def test_ceo_fraud_scenario(client):
    """Test the ceo fraud scenario page."""
    response = client.get('/ceo-fraud')
    assert response.status_code == 200

def test_ceo_fraud_scenario_result(client):
    """Test the ceo fraud scenario result."""
    response = client.get('/ceo-fraud/result')
    assert response.status_code == 200


def test_tech_support_scenario(client):
    """Test the tech support scenario page."""
    response = client.get('/tech-support')
    assert response.status_code == 200

def test_tech_support_scenario_result(client):
    """Test the tech support scenario result."""
    response = client.get('/tech-support/result')
    assert response.status_code == 200


def test_social_media_scenario(client):
    """Test the social media scenario page."""
    response = client.get('/social-media')
    assert response.status_code == 200

def test_social_media_scenario_result(client):
    """Test the social media scenario result."""
    response = client.get('/social-media/result')
    assert response.status_code == 200


def test_fraud_payment_scenario(client):
    """Test the fraud payment scenario page."""
    response = client.get('/fraud-payment')
    assert response.status_code == 200

def test_fraud_payment_scenario_result(client):
    """Test the fraud payment scenario result."""
    response = client.get('/fraud-payment/result')
    assert response.status_code == 200