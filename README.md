# Cancer Data Visualization Dashboard

A Flask web application for visualizing Australian cancer incidence and mortality data with interactive maps, charts, and analytics.

## Features

- **Interactive Dashboard** - Choropleth maps, time series charts, and heatmaps
- **Advanced Analytics** - Trend analysis, outlier detection, and correlations
- **RESTful API** - JSON endpoints for data access
- **Responsive Design** - Works on all devices

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

4. **Access Dashboard**
   - Main Dashboard: http://localhost:5000
   - Analytics: http://localhost:5000/analytics
   - API Health: http://localhost:5000/api/health

## Environment Variables

```env
DB_HOST=your-database-host
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name
```

## API Endpoints

- `GET /api/data` - Cancer data with filters
- `GET /api/states` - List of states
- `GET /api/analytics/trends` - Trend analysis
- `GET /api/analytics/outliers` - Outlier detection

## Tech Stack

- **Backend**: Flask, PostgreSQL, Pandas
- **Frontend**: Bootstrap, Plotly, Folium
- **Analytics**: NumPy, Statistical analysis