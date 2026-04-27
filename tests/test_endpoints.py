import json
import pytest
from app import WEATHER_CONDITIONS


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""

    def test_health_endpoint_returns_200(self, client):
        """Test that health endpoint returns 200 status."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_correct_json(self, client):
        """Test that health endpoint returns correct JSON structure."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data == {"status": "healthy"}


class TestPredictEndpoint:
    """Test cases for the weather prediction endpoint."""

    def test_predict_with_valid_city(self, client):
        """Test prediction with a valid city name."""
        response = client.post('/predict',
                             json={"city": "London"},
                             content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "city" in data
        assert "prediction" in data
        assert data["city"] == "London"
        assert data["prediction"] in WEATHER_CONDITIONS

    def test_predict_with_empty_city(self, client):
        """Test prediction with empty city name."""
        response = client.post('/predict',
                             json={"city": ""},
                             content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "City name is required"

    def test_predict_with_whitespace_city(self, client):
        """Test prediction with whitespace-only city name."""
        response = client.post('/predict',
                             json={"city": "   "},
                             content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "City name is required"

    def test_predict_without_city_key(self, client):
        """Test prediction without city key in JSON."""
        response = client.post('/predict',
                             json={},
                             content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "City name is required"

    def test_predict_with_invalid_json(self, client):
        """Test prediction with invalid JSON."""
        response = client.post('/predict',
                             data="invalid json",
                             content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Invalid JSON"

    def test_predict_method_not_allowed(self, client):
        """Test that GET method is not allowed on predict endpoint."""
        response = client.get('/predict')
        assert response.status_code == 405

    def test_weather_conditions_are_valid(self, client):
        """Test that all returned predictions are from the valid weather conditions."""
        # Test multiple times to ensure randomness doesn't break validation
        for _ in range(10):
            response = client.post('/predict',
                                 json={"city": "TestCity"},
                                 content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["prediction"] in WEATHER_CONDITIONS


class TestWeatherConditions:
    """Test cases for weather conditions configuration."""

    def test_weather_conditions_not_empty(self):
        """Test that weather conditions list is not empty."""
        assert len(WEATHER_CONDITIONS) > 0

    def test_weather_conditions_are_strings(self):
        """Test that all weather conditions are strings."""
        for condition in WEATHER_CONDITIONS:
            assert isinstance(condition, str)

    def test_weather_conditions_unique(self):
        """Test that weather conditions are unique."""
        assert len(WEATHER_CONDITIONS) == len(set(WEATHER_CONDITIONS))