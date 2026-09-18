import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.concurrency import run_in_threadpool

from app.db.database import SessionLocal
from app.services.analytics_service import get_analytics


router = APIRouter(
    prefix="/api/ws",
    tags=["WebSocket"],
)

ALLOWED_PERIODS = {"today", "7d", "30d"}
DEFAULT_PERIOD = "today"
PUSH_INTERVAL_SECONDS = 3


def normalize_period(value: str | None) -> str:
    if value in ALLOWED_PERIODS:
        return value
    return DEFAULT_PERIOD


def load_analytics(period: str) -> dict:
    db = SessionLocal()
    try:
        analytics = get_analytics(db, period=period)
        return analytics.model_dump(mode="json")
    finally:
        db.close()


class AnalyticsStreamState:
    def __init__(self, period: str) -> None:
        self.period = normalize_period(period)
        self.changed = asyncio.Event()

    def set_period(self, value: str | None) -> None:
        new_period = normalize_period(value)
        if new_period != self.period:
            self.period = new_period
            self.changed.set()


async def receive_loop(websocket: WebSocket, state: AnalyticsStreamState) -> None:
    while True:
        message = await websocket.receive_json()
        if isinstance(message, dict) and message.get("type") == "set_period":
            state.set_period(message.get("period"))


async def send_loop(websocket: WebSocket, state: AnalyticsStreamState) -> None:
    while True:
        period = state.period
        state.changed.clear()

        try:
            data = await run_in_threadpool(load_analytics, period)
        except Exception:
            await websocket.send_json(
                {
                    "type": "error",
                    "period": period,
                    "message": "Failed to load analytics",
                }
            )
            await asyncio.sleep(PUSH_INTERVAL_SECONDS)
            continue

        await websocket.send_json(
            {
                "type": "analytics",
                "period": period,
                "data": data,
            }
        )

        try:
            await asyncio.wait_for(
                state.changed.wait(),
                timeout=PUSH_INTERVAL_SECONDS,
            )
        except asyncio.TimeoutError:
            pass


@router.websocket("/analytics")
async def analytics_websocket(
    websocket: WebSocket,
    period: str = DEFAULT_PERIOD,
):
    await websocket.accept()

    state = AnalyticsStreamState(period)

    receiver = asyncio.create_task(receive_loop(websocket, state))
    sender = asyncio.create_task(send_loop(websocket, state))

    try:
        done, pending = await asyncio.wait(
            {receiver, sender},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        for task in done:
            exception = task.exception()
            if exception and not isinstance(exception, WebSocketDisconnect):
                raise exception

    except WebSocketDisconnect:
        pass

    finally:
        receiver.cancel()
        sender.cancel()