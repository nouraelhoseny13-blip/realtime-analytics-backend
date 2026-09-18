from app.db.database import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(
        text("""
            ALTER TABLE analytics
            ADD COLUMN IF NOT EXISTS endpoint VARCHAR(255)
            NOT NULL DEFAULT '/api/analytics'
        """)
    )

print("Endpoint column added successfully!")