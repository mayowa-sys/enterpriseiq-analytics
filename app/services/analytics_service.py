from bson import ObjectId
from datetime import datetime, timedelta
from app.db import db

async def get_peak_hours(org_id: str) -> list:
    pipeline = [
        {
            "$match": {
                "orgId": ObjectId(org_id),
                "status": {"$in": ["completed", "confirmed", "pending"]}
            }
        },
        {
            "$group": {
                "_id": {"$hour": "$startTime"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    results = await db.appointments.aggregate(pipeline).to_list(24)
    return [{"hour": r["_id"], "count": r["count"]} for r in results]


async def get_no_show_rate(org_id: str) -> dict:
    total = await db.appointments.count_documents({
        "orgId": ObjectId(org_id)
    })

    cancelled = await db.appointments.count_documents({
        "orgId": ObjectId(org_id),
        "status": "cancelled"
    })

    rate = round((cancelled / total) * 100, 2) if total > 0 else 0

    return {
        "total": total,
        "cancelled": cancelled,
        "noShowRate": rate
    }


async def get_staff_utilisation(org_id: str, start_date: str = None, end_date: str = None) -> list:
    match_query = {"orgId": ObjectId(org_id)}

    if start_date and end_date:
        match_query["startTime"] = {
            "$gte": datetime.fromisoformat(start_date),
            "$lte": datetime.fromisoformat(end_date)
        }

    pipeline = [
        {"$match": match_query},
        {
            "$group": {
                "_id": "$staffId",
                "totalAppointments": {"$sum": 1},
                "totalMinutes": {
                    "$sum": {
                        "$divide": [
                            {"$subtract": ["$endTime", "$startTime"]},
                            60000
                        ]
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "_id",
                "as": "staffInfo"
            }
        },
        {"$unwind": "$staffInfo"},
        {"$sort": {"totalMinutes": -1}}
    ]

    results = await db.appointments.aggregate(pipeline).to_list(100)

    return [
        {
            "staffId": str(r["_id"]),
            "staffName": f"{r['staffInfo']['firstName']} {r['staffInfo']['lastName']}",
            "totalAppointments": r["totalAppointments"],
            "totalHours": round(r["totalMinutes"] / 60, 2)
        }
        for r in results
    ]

async def get_volume_trend(org_id: str) -> list:
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    pipeline = [
        {
            "$match": {
                "orgId": ObjectId(org_id),
                "createdAt": {"$gte": thirty_days_ago}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$createdAt"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    results = await db.appointments.aggregate(pipeline).to_list(30)
    return [{"date": r["_id"], "count": r["count"]} for r in results]


async def get_revenue_estimate(org_id: str) -> dict:
    # Get org settings for appointment type pricing
    org = await db.organisations.find_one({"_id": ObjectId(org_id)})

    if not org:
        return {"data": [], "totalEstimatedRevenue": 0}

    # Build price map from org settings
    price_map = {}
    if org.get("settings") and org["settings"].get("appointmentTypes"):
        for apt_type in org["settings"]["appointmentTypes"]:
            price_map[apt_type["name"]] = apt_type["priceNaira"]

    pipeline = [
        {
            "$match": {
                "orgId": ObjectId(org_id),
                "status": {"$in": ["completed", "confirmed"]}
            }
        },
        {
            "$group": {
                "_id": "$type",
                "count": {"$sum": 1}
            }
        }
    ]

    results = await db.appointments.aggregate(pipeline).to_list(20)

    revenue_data = []
    total_revenue = 0

    for r in results:
        apt_type = r["_id"]
        count = r["count"]
        price = price_map.get(apt_type, 0)
        type_revenue = count * price

        revenue_data.append({
            "appointmentType": apt_type,
            "count": count,
            "pricePerAppointment": price,
            "totalRevenue": type_revenue
        })

        total_revenue += type_revenue

    return {
        "data": revenue_data,
        "totalEstimatedRevenue": total_revenue
    }


async def get_summary(org_id: str) -> dict:
    total = await db.appointments.count_documents({
        "orgId": ObjectId(org_id)
    })

    completed = await db.appointments.count_documents({
        "orgId": ObjectId(org_id), "status": "completed"
    })

    cancelled = await db.appointments.count_documents({
        "orgId": ObjectId(org_id), "status": "cancelled"
    })

    no_show_rate = round((cancelled / total) * 100, 2) if total > 0 else 0

    total_staff = await db.users.count_documents({
        "orgId": ObjectId(org_id), "role": "staff"
    })

    # Get peak hour
    peak_hours = await get_peak_hours(org_id)
    peak_hour = None
    if peak_hours:
        peak_hour = max(peak_hours, key=lambda x: x["count"])["hour"]

    # Get revenue
    revenue_data = await get_revenue_estimate(org_id)

    return {
        "totalAppointments": total,
        "completedAppointments": completed,
        "cancelledAppointments": cancelled,
        "noShowRate": no_show_rate,
        "peakHour": peak_hour,
        "totalStaff": total_staff,
        "totalEstimatedRevenue": revenue_data["totalEstimatedRevenue"]
    }