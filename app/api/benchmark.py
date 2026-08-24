import math
import random

from app.api.benchmark_repository import get_benchmark_aggregate

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/benchmark",
    tags=["benchmark"],
)


# ============================================================
# PG-27 Configuration
# ============================================================

MIN_PEER_GROUP_SIZE = 10


# ============================================================
# PG-26 Configuration
# ============================================================

# Keep privacy parameters server-side.
# Change these only if the team provides a different
# calibrated epsilon/sensitivity requirement.
EPSILON = 1.0
SENSITIVITY = 100.0


# ============================================================
# Request Schema
# ============================================================

class BenchmarkRequest(BaseModel):
    """
    Client sends only cohort information.

    Raw peer scores must NOT be supplied by the client.
    """

    industry: str = Field(min_length=1)
    region: str = Field(min_length=1)
    size_band: str = Field(min_length=1)


# ============================================================
# Response Schema
# ============================================================

class BenchmarkResponse(BaseModel):
    industry: str
    region: str
    size_band: str

    peer_count: int

    peer_25th: float
    peer_median: float
    peer_75th: float


# ============================================================
# PG-26: Laplace Noise
# ============================================================

def generate_laplace_noise(
    scale: float,
) -> float:
    """
    Generate Laplace-distributed noise.
    """

    u = random.uniform(-0.5, 0.5)

    if u == 0:
        u = 1e-12

    return -scale * math.copysign(
        math.log(1 - 2 * abs(u)),
        u,
    )


def apply_laplace_noise(
    value: float,
) -> float:
    """
    Apply calibrated Laplace noise and keep
    the resulting security score within 0-100.
    """

    scale = SENSITIVITY / EPSILON

    noisy_value = (
        value
        + generate_laplace_noise(scale)
    )

    noisy_value = max(
        0.0,
        min(100.0, noisy_value),
    )

    return round(noisy_value, 2)




# ============================================================
# POST /benchmark
# ============================================================

@router.post(
    "",
    response_model=BenchmarkResponse,
)
async def create_benchmark(
    request: BenchmarkRequest,
) -> BenchmarkResponse:

    # --------------------------------------------------------
    # Step 1:
    # Query benchmark_aggregate
    # --------------------------------------------------------

    peer = await get_benchmark_aggregate(
        industry=request.industry,
        region=request.region,
        size_band=request.size_band,
    )

    # --------------------------------------------------------
    # Cohort does not exist
    # --------------------------------------------------------

    if peer is None:
        raise HTTPException(
            status_code=404,
            detail="benchmark cohort not found",
        )

    peer_count = int(peer["peer_count"])

    # --------------------------------------------------------
    # Step 2:
    # PG-27 - Minimum Peer Group Enforcement
    # --------------------------------------------------------

    if peer_count < MIN_PEER_GROUP_SIZE:
        raise HTTPException(
            status_code=422,
            detail="insufficient peers",
        )

    # --------------------------------------------------------
    # Make sure percentile values exist
    # --------------------------------------------------------

    if (
        peer["peer_25th"] is None
        or peer["peer_median"] is None
        or peer["peer_75th"] is None
    ):
        raise HTTPException(
            status_code=500,
            detail="benchmark metrics unavailable",
        )

    # --------------------------------------------------------
    # Step 3:
    # PG-26 - Differential Privacy
    #
    # Apply Laplace noise to:
    # p25 / p50 / p75
    # --------------------------------------------------------

    noisy_25th = apply_laplace_noise(
        float(peer["peer_25th"])
    )

    noisy_median = apply_laplace_noise(
        float(peer["peer_median"])
    )

    noisy_75th = apply_laplace_noise(
        float(peer["peer_75th"])
    )

    # --------------------------------------------------------
    # Step 4:
    # Return privacy-preserving metrics
    # --------------------------------------------------------

    return BenchmarkResponse(
        industry=peer["industry"],
        region=peer["region"],
        size_band=peer["size_band"],
        peer_count=peer_count,
        peer_25th=noisy_25th,
        peer_median=noisy_median,
        peer_75th=noisy_75th,
    )