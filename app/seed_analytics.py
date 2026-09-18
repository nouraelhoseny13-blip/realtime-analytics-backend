import random
from datetime import datetime, timedelta, timezone

from app.db.database import SessionLocal
from app.models import Analytics


def seed_analytics():
    db = SessionLocal()

    try:
        db.query(Analytics).delete()

        now = datetime.now(timezone.utc)

        services = [
            ("API Gateway", 0.9982, 84),
            ("Auth Service", 0.9994, 61),
            ("Analytics Engine", 0.9971, 112),
            ("Notification Service", 0.9896, 143),
        ]

        total_hours = 30 * 24

        records = []

        for hour_offset in range(total_hours):
            timestamp = now - timedelta(hours=total_hours - 1 - hour_offset)

            day_index = hour_offset // 24
            hour_of_day = hour_offset % 24

            day_growth = day_index * 4
            daily_cycle = abs(12 - hour_of_day)

            for service_index, (service, base_success_rate, base_response_time) in enumerate(
                services
            ):
                active_users = (
                    280
                    + day_growth
                    + (hour_of_day * 12)
                    + (service_index * 25)
                    + random.randint(-15, 15)
                )

                requests_per_minute = (
                    350
                    + (day_growth * 6)
                    + (hour_of_day * 30)
                    + (service_index * 50)
                    + random.randint(-30, 30)
                )

                requests_per_minute = max(requests_per_minute, 50)

                total_requests = requests_per_minute * 60

                success_rate = min(
                    base_success_rate * 100 + random.uniform(-0.3, 0.2),
                    99.99,
                )

                response_time = max(
                    base_response_time + random.randint(-10, 20) + daily_cycle,
                    20,
                )

                record = Analytics(
                    timestamp=timestamp,
                    active_users=active_users,
                    requests_per_minute=requests_per_minute,
                    success_rate=round(success_rate, 2),
                    error_rate=round(100 - success_rate, 2),
                    average_response_time=response_time,
                    total_requests=total_requests,
                    service=service,
                )

                records.append(record)

        db.add_all(records)
        db.commit()

        print(
            f"Successfully inserted {len(records)} analytics records "
            f"spanning {total_hours} hours ({total_hours // 24} days)."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_analytics()