from datetime import datetime, timedelta, timezone

from app.db.database import SessionLocal
from app.models import Analytics


def seed_analytics():
    db = SessionLocal()

    try:
        db.query(Analytics).delete()

        now = datetime.now(timezone.utc)

        services = [
            ("API Gateway", 99.82, 84, "/api/analytics"),
            ("Auth Service", 99.94, 61, "/api/auth/login"),
            ("Analytics Engine", 99.71, 112, "/api/activity"),
            ("Notification Service", 98.96, 143, "/api/notifications"),
        ]

        records = []

        # 30 days × 24 hours × 4 services = 2880 records
        for hour in range(30 * 24):

            timestamp = now - timedelta(
                hours=(30 * 24 - 1 - hour)
            )

            for service_index, (
                service,
                success_rate,
                response_time,
                endpoint,
            ) in enumerate(services):

                active_users = (
                    300
                    + (hour % 24) * 15
                    + (service_index * 25)
                )

                requests_per_minute = (
                    400
                    + (hour % 24) * 35
                    + (service_index * 50)
                )

                total_requests = requests_per_minute * 60

                record = Analytics(
                    timestamp=timestamp,
                    active_users=active_users,
                    requests_per_minute=requests_per_minute,
                    success_rate=success_rate,
                    error_rate=round(
                        100 - success_rate,
                        2,
                    ),
                    average_response_time=response_time,
                    total_requests=total_requests,
                    service=service,
                    endpoint=endpoint,
                )

                records.append(record)

        db.add_all(records)
        db.commit()

        print(
            f"Successfully inserted {len(records)} analytics records."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_analytics()