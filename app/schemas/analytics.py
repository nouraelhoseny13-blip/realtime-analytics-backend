from datetime import datetime

from pydantic import BaseModel


class AnalyticsStats(BaseModel):

    activeUsers: int

    requestsPerMinute: int

    peakTraffic: int

    successRate: float

    averageResponseTime: int

    totalRequests: int

    errorRate: float


class TrafficPoint(BaseModel):

    timestamp: str

    requests: int

    users: int

    errorRate: float

    responseTime: int


class ServicePerformance(BaseModel):

    service: str

    requests: int

    successRate: float

    averageResponseTime: int


class EndpointPerformance(BaseModel):

    endpoint: str

    requests: int


class AnalyticsResponse(BaseModel):

    stats: AnalyticsStats

    traffic: list[TrafficPoint]

    services: list[ServicePerformance]

    endpoints: list[EndpointPerformance]

    period: str

    updatedAt: datetime