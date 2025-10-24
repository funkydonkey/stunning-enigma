"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestFormatEndpoint:
    """Tests for /format endpoint."""

    def test_format_simple_formula(self):
        """Test formatting a simple formula."""
        response = client.post(
            "/format",
            json={"formula": "=IF(A1>0,\"Yes\",\"No\")"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "pretty" in data
        assert data["pretty"].startswith("=")

    def test_format_nested_formula(self):
        """Test formatting a nested formula."""
        response = client.post(
            "/format",
            json={"formula": "=IF(A1>0,IF(B1<10,\"OK\",\"NO\"),\"FAIL\")"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "pretty" in data
        assert "\n" in data["pretty"]  # Should have line breaks

    def test_format_empty_formula(self):
        """Test formatting empty formula returns error."""
        response = client.post(
            "/format",
            json={"formula": ""}
        )
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_format_invalid_parentheses(self):
        """Test formatting formula with unbalanced parentheses."""
        response = client.post(
            "/format",
            json={"formula": "=IF(A1>0,\"Yes\",\"No\""}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "parenthes" in data["detail"].lower()

    def test_format_missing_formula_field(self):
        """Test request without formula field."""
        response = client.post(
            "/format",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestSimplifyEndpoint:
    """Tests for /simplify endpoint."""

    @pytest.mark.skip(reason="Requires valid API key and makes external API call")
    def test_simplify_formula(self):
        """Test simplifying a formula with AI."""
        response = client.post(
            "/simplify",
            json={"formula": "=IF(A1>0,IF(B1<10,\"OK\",\"NO\"),\"FAIL\")"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "pretty" in data
        assert "simplified" in data
        assert "comment" in data

    def test_simplify_empty_formula(self):
        """Test simplifying empty formula returns error."""
        response = client.post(
            "/simplify",
            json={"formula": ""}
        )
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_simplify_invalid_parentheses(self):
        """Test simplifying formula with unbalanced parentheses."""
        response = client.post(
            "/simplify",
            json={"formula": "=IF(A1>0,\"Yes\",\"No\""}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_simplify_missing_formula_field(self):
        """Test request without formula field."""
        response = client.post(
            "/simplify",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.options(
            "/format",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert "access-control-allow-origin" in response.headers
