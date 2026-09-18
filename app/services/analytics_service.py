from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Analytics
from app.schemas.analytics import (
    AnalyticsResponse,
    AnalyticsStats,
    EndpointPerformance,
    ServicePerformance,
    TrafficPoint,
)


def get_analytics(
    db: Session,
    period: str = "today",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    service: Optional[str] = None,
) -> AnalyticsResponse:

    now = datetime.now(timezone.utc)

    if period == "7d":
        start_time = now - timedelta(days=7)

    elif period == "30d":
        start_time = now - timedelta(days=30)

    elif period == "custom":
        if start_date:
            start_time = datetime.fromisoformat(
                start_date
            ).replace(tzinfo=timezone.utc)
        else:
            start_time = now - timedelta(hours=24)

    else:
        start_time = now - timedelta(hours=24)

    query = (
        db.query(Analytics)
        .filter(Analytics.timestamp >= start_time)
    )

    if period == "custom" and end_date:
        end_time = datetime.fromisoformat(
            end_date
        ).replace(tzinfo=timezone.utc)

        query = query.filter(
            Analytics.timestamp <= end_time
        )

    if service:
        query = query.filter(
            Analytics.service == service
        )

    records = (
        query
        .order_by(Analytics.timestamp.asc())
        .all()
    )

    if not records:
        stats = AnalyticsStats(
            activeUsers=0,
            requestsPerMinute=0,
            peakTraffic=0,
            successRate=0.0,
            averageResponseTime=0,
            totalRequests=0,
            errorRate=0.0,
        )

        return AnalyticsResponse(
            stats=stats,
            traffic=[],
            services=[],
            endpoints=[],
            period=period,
            updatedAt=now,
        )

    latest = records[-1]

    total_requests = sum(
        record.total_requests
        for record in records
    )

    active_users = round(
        sum(
            record.active_users
            for record in records
        ) / len(records)
    )

    requests_per_minute = round(
        sum(
            record.requests_per_minute
            for record in records
        ) / len(records)
    )

    peak_traffic = max(
        record.requests_per_minute
        for record in records
    )

    success_rate = round(
        sum(
            record.success_rate
            for record in records
        ) / len(records),
        2,
    )

    average_response_time = round(
        sum(
            record.average_response_time
            for record in records
        ) / len(records)
    )

    error_rate = round(
        100 - success_rate,
        2,
    )

    stats = AnalyticsStats(
        activeUsers=active_users,
        requestsPerMinute=requests_per_minute,
        peakTraffic=peak_traffic,
        successRate=success_rate,
        averageResponseTime=average_response_time,
        totalRequests=total_requests,
        errorRate=error_rate,
    )

    traffic = [
        TrafficPoint(
            timestamp=record.timestamp.strftime("%H:%M"),
            requests=record.requests_per_minute,
            users=record.active_users,
            errorRate=round(
                100 - record.success_rate,
                2,
            ),
            responseTime=record.average_response_time,
        )
        for record in records
    ]

    # -----------------------------
    # Group analytics by service
    # -----------------------------

    service_groups: dict[str, list[Analytics]] = {}

    for record in records:
        service_groups.setdefault(
            record.service,
            [],
        ).append(record)

    services = []

    for service_name, service_records in service_groups.items():

        service_requests = sum(
            record.total_requests
            for record in service_records
        )

        service_success_rate = round(
            sum(
                record.success_rate
                for record in service_records
            ) / len(service_records),
            2,
        )

        service_response_time = round(
            sum(
                record.average_response_time
                for record in service_records
            ) / len(service_records)
        )

        services.append(
            ServicePerformance(
                service=service_name,
                requests=service_requests,
                successRate=service_success_rate,
                averageResponseTime=service_response_time,
            )
        )

    # -----------------------------
    # Group analytics by endpoint
    # -----------------------------

    endpoint_groups: dict[str, list[Analytics]] = {}

    for record in records:
        endpoint_groups.setdefault(
            record.endpoint,
            [],
        ).append(record)

    endpoints = []

    for endpoint_name, endpoint_records in endpoint_groups.items():

        endpoint_requests = sum(
            record.total_requests
            for record in endpoint_records
        )

        endpoints.append(
            EndpointPerformance(
                endpoint=endpoint_name,
                requests=endpoint_requests,
            )
        )

    # Sort endpoints by request count
    endpoints.sort(
        key=lambda item: item.requests,
        reverse=True,
    )

    return AnalyticsResponse(
        stats=stats,
        traffic=traffic,
        services=services,
        endpoints=endpoints,
        period=period,
        updatedAt=latest.timestamp,
    )