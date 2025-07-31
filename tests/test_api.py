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

def test_analytics_trends(client):
    """Test trends analytics endpoint."""
    response = client.get('/api/analytics/trends')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data

def test_analytics_top_states(client):
    """Test top states analytics endpoint."""
    response = client.get('/api/analytics/top-states')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data

def test_analytics_outliers(client):
    """Test outliers analytics endpoint."""
    response = client.get('/api/analytics/outliers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data

def test_analytics_correlations(client):
    """Test correlations analytics endpoint."""
    response = client.get('/api/analytics/correlations')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data

def test_analytics_compare_states(client):
    """Test compare states analytics endpoint."""
    payload = {
        'states': ['New South Wales', 'Victoria'],
        'metric': 'mortality_rate'
    }
    response = client.post('/api/analytics/compare-states',
                         data=json.dumps(payload),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
