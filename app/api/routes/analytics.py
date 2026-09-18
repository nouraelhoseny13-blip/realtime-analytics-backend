from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import get_analytics


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get(
    "",
    response_model=AnalyticsResponse,
)
def analytics(
    period: str = Query("today"),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
    service: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return get_analytics(
        db=db,
        period=period,
        start_date=startDate,
        end_date=endDate,
        service=service,
    )