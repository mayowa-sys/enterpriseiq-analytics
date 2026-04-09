import os
from fastapi import APIRouter, Header, HTTPException, Query
from typing import Optional
from app.services import analytics_service

router = APIRouter()

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

def verify_internal_key(x_internal_key: str = Header(...)):
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal API key")
    return x_internal_key


@router.get("/peak-hours")
async def peak_hours(
    org_id: str = Query(..., description="Organisation ID"),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_peak_hours(org_id)
    return {"status": "success", "data": data, "orgId": org_id}


@router.get("/no-show-rate")
async def no_show_rate(
    org_id: str = Query(..., description="Organisation ID"),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_no_show_rate(org_id)
    return {"status": "success", "data": data, "orgId": org_id}


@router.get("/staff-utilisation")
async def staff_utilisation(
    org_id: str = Query(..., description="Organisation ID"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_staff_utilisation(org_id, start_date, end_date)
    return {"status": "success", "data": data, "orgId": org_id}


@router.get("/volume-trend")
async def volume_trend(
    org_id: str = Query(..., description="Organisation ID"),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_volume_trend(org_id)
    return {"status": "success", "data": data, "orgId": org_id}


@router.get("/revenue-estimate")
async def revenue_estimate(
    org_id: str = Query(..., description="Organisation ID"),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_revenue_estimate(org_id)
    return {"status": "success", "data": data, "orgId": org_id}


@router.get("/summary")
async def summary(
    org_id: str = Query(..., description="Organisation ID"),
    x_internal_key: str = Header(...)
):
    verify_internal_key(x_internal_key)
    data = await analytics_service.get_summary(org_id)
    return {"status": "success", "data": data, "orgId": org_id}