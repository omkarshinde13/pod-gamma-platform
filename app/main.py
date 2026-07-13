from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

try:
    from app.anonymizer import process_analytics_pipeline
    from app.streak import evaluate_user_streak
except ImportError:
    def process_analytics_pipeline(data):
        return {"status": "Mocked Isolation Mode", "records_parsed": len(data)}

    def evaluate_user_streak(l, c, s):
        return {"status": "Mocked Isolation Mode", "current_streak": s}

app = FastAPI(
    title="Pod Gamma Asynchronous Gateway Engine",
    description="Production-Ready Secure Routing Gateway for Module 4"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ScoreInputItem(BaseModel):
    client_id: str = Field(..., min_length=3, max_length=50, description="Unique corporate identifier")
    security_score: float = Field(..., ge=0.0, le=100.0, description="Raw engineering metrics score")

class StreamAnalyticsPayload(BaseModel):
    stream: List[ScoreInputItem]

class StreakVerificationPayload(BaseModel):
    last_log: str = Field(..., description="Timestamp of previous platform log")
    current_log: str = Field(..., description="Timestamp of current engagement transaction")
    current_streak: int = Field(..., ge=0, description="Active user streak count")

synthetic_db_records = [
    {"client_id": f"COMP_ID_{i}", "security_score": float(65.0 + (i % 30))}
    for i in range(1, 51)
]

@app.get("/health", status_code=status.HTTP_200_OK)
def verify_system_health():
    return {"status": "healthy"}

@app.post("/api/v1/analytics", status_code=status.HTTP_200_OK)
def process_benchmarks_gateway(payload: StreamAnalyticsPayload):
    data_stream = [
        {"client_id": item.client_id, "security_score": item.security_score}
        for item in payload.stream
    ]

    if not data_stream:
        data_stream = synthetic_db_records

    return process_analytics_pipeline(data_stream)

@app.post("/api/v1/streaks", status_code=status.HTTP_200_OK)
def process_gamification_streaks(payload: StreakVerificationPayload):
    return evaluate_user_streak(
        payload.last_log,
        payload.current_log,
        payload.current_streak
    )