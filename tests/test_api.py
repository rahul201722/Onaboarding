"""
Test API endpoints.
"""
import pytest
import json

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_states(client):
    """Test get states endpoint."""
    response = client.get('/api/states')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data

def test_get_cancer_types(client):
    """Test get cancer types endpoint."""
    response = client.get('/api/cancer-types')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data

def test_get_years(client):
    """Test get years endpoint."""
    response = client.get('/api/years')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data

def test_get_data_with_filters(client):
    """Test get data endpoint with filters."""
    response = client.get('/api/data?state=New South Wales&year=2020')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data
