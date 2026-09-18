from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api",
    tags=["Activity"],
)


@router.get("/activity")
def get_activity(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    service: str | None = None,
    status: str | None = None,
):
    activities = [
        {
            "id": "activity-1",
            "service": "API",
            "action": "Request processed",
            "status": "success",
            "message": "GET /api/analytics",
            "timestamp": "2026-09-17T01:00:00",
        },
        {
            "id": "activity-2",
            "service": "Auth",
            "action": "User login",
            "status": "success",
            "message": "User authenticated successfully",
            "timestamp": "2026-09-17T00:59:30",
        },
        {
            "id": "activity-3",
            "service": "Analytics",
            "action": "Data updated",
            "status": "success",
            "message": "Analytics data refreshed",
            "timestamp": "2026-09-17T00:59:00",
        },
        {
            "id": "activity-4",
            "service": "API",
            "action": "Request failed",
            "status": "error",
            "message": "GET /api/users",
            "timestamp": "2026-09-17T00:58:20",
        },
        {
            "id": "activity-5",
            "service": "Database",
            "action": "Query completed",
            "status": "success",
            "message": "Analytics query completed",
            "timestamp": "2026-09-17T00:57:45",
        },
    ]

    if service:
        activities = [
            item
            for item in activities
            if item["service"].lower()
            == service.lower()
        ]

    if status:
        activities = [
            item
            for item in activities
            if item["status"].lower()
            == status.lower()
        ]

    activities = activities[:limit]

    return {
        "items": activities,
        "total": len(activities),
    }