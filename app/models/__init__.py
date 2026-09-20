```python
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


class Analytics(Base):
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    active_users: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    requests_per_minute: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    success_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    error_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    average_response_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_requests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    endpoint: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="/api/analytics",
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
```
