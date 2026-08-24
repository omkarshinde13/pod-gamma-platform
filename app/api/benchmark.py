from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/benchmark",
    tags=["benchmark"],
)


class BenchmarkRequest(BaseModel):
    industry: str
    region: str
    size_band: str


class BenchmarkResponse(BaseModel):
    industry: str
    region: str
    size_band: str
    peer_count: int
    peer_25th: float | None = None
    peer_median: float | None = None
    peer_75th: float | None = None


@router.post("", response_model=BenchmarkResponse)
async def create_benchmark(request: BenchmarkRequest) -> BenchmarkResponse:
    return BenchmarkResponse(
        industry=request.industry,
        region=request.region,
        size_band=request.size_band,
        peer_count=0,
        peer_25th=None,
        peer_median=None,
        peer_75th=None,
    )