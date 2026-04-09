# EnterpriseIQ Analytics Service

Internal Python microservice that generates business intelligence from EnterpriseIQ's appointment data using MongoDB aggregation pipelines.

## Live URL
- **Swagger Docs:** `web-production-12be9.up.railway.app`
- **Main API Repo:** https://github.com/mayowa-sys/enterpriseiq-api

## What It Does

This service reads from the same MongoDB database as the Node.js API and runs aggregation pipelines to answer business questions:

- When are we busiest? (peak hours)
- How many appointments are being cancelled? (no-show rate)
- How is each staff member being utilised?
- How many appointments are being booked per day?
- How much revenue are we generating per appointment type?

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database Driver | Motor (async MongoDB) |
| Validation | Pydantic |
| Server | Uvicorn |
| Deployment | Railway |

## Security

This service is internal — it is not meant to be called directly by clients. Every endpoint requires an `x-internal-key` header that must match the shared secret configured in both services. The Node.js API proxies all analytics requests and handles user authentication.

## Endpoints

```
GET /health
GET /analytics/summary
GET /analytics/peak-hours
GET /analytics/no-show-rate
GET /analytics/staff-utilisation
GET /analytics/volume-trend
GET /analytics/revenue-estimate
```

All endpoints require:
- Query param: `org_id` — the organisation's MongoDB ObjectId
- Header: `x-internal-key` — shared internal API key

## Getting Started

### Prerequisites
- Python 3.11+
- MongoDB (same instance as the Node.js API)

### Setup

```bash
git clone https://github.com/mayowa-sys/enterpriseiq-analytics
cd enterpriseiq-analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your .env values
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

```
MONGODB_URI=mongodb://localhost:27017/enterpriseiq
INTERNAL_API_KEY=your_internal_key
PORT=8000
```

## Example Response

`GET /analytics/summary?org_id=<id>`

```json
{
  "status": "success",
  "data": {
    "totalAppointments": 24,
    "completedAppointments": 8,
    "cancelledAppointments": 3,
    "noShowRate": 12.5,
    "peakHour": 10,
    "totalStaff": 3,
    "totalEstimatedRevenue": 45000
  },
  "orgId": "69d7009fd683e4f511052d43"
}
```