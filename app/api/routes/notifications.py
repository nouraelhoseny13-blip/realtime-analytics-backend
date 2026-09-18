from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api",
    tags=["Notifications"],
)


@router.get("/notifications")
def get_notifications(
    unreadOnly: bool = Query(default=False),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):
    notifications = [
        {
            "id": "notification-1",
            "title": "High traffic detected",
            "message": "Traffic increased by 18% in the last hour.",
            "type": "warning",
            "read": False,
            "timestamp": "2026-09-17T01:00:00",
        },
        {
            "id": "notification-2",
            "title": "Analytics updated",
            "message": "Analytics data has been refreshed successfully.",
            "type": "success",
            "read": True,
            "timestamp": "2026-09-17T00:59:30",
        },
        {
            "id": "notification-3",
            "title": "API response time",
            "message": "Average response time is above the normal threshold.",
            "type": "warning",
            "read": False,
            "timestamp": "2026-09-17T00:58:45",
        },
        {
            "id": "notification-4",
            "title": "System healthy",
            "message": "All services are operating normally.",
            "type": "info",
            "read": True,
            "timestamp": "2026-09-17T00:57:20",
        },
    ]

    if unreadOnly:
        notifications = [
            item
            for item in notifications
            if not item["read"]
        ]

    notifications = notifications[:limit]

    unreadCount = sum(
        1
        for item in notifications
        if not item["read"]
    )

    return {
        "items": notifications,
        "total": len(notifications),
        "unreadCount": unreadCount,
    }