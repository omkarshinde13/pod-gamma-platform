BENCHMARK_DATA = [
    {
        "industry": "Technology",
        "region": "West",
        "size_band": "Large",
        "peer_count": 20,
        "peer_25th": 65.20,
        "peer_median": 76.40,
        "peer_75th": 88.10,
    },
    {
        "industry": "Technology",
        "region": "West",
        "size_band": "Medium",
        "peer_count": 18,
        "peer_25th": 61.30,
        "peer_median": 72.50,
        "peer_75th": 84.70,
    },
    {
        "industry": "Technology",
        "region": "North",
        "size_band": "Large",
        "peer_count": 16,
        "peer_25th": 62.50,
        "peer_median": 75.10,
        "peer_75th": 87.30,
    },
    {
        "industry": "Finance",
        "region": "West",
        "size_band": "Large",
        "peer_count": 15,
        "peer_25th": 60.10,
        "peer_median": 71.20,
        "peer_75th": 83.50,
    },
    {
        "industry": "Finance",
        "region": "North",
        "size_band": "Medium",
        "peer_count": 19,
        "peer_25th": 64.20,
        "peer_median": 73.60,
        "peer_75th": 85.40,
    },
    {
        "industry": "Healthcare",
        "region": "West",
        "size_band": "Large",
        "peer_count": 17,
        "peer_25th": 63.40,
        "peer_median": 74.80,
        "peer_75th": 86.20,
    },
    {
        "industry": "Healthcare",
        "region": "South",
        "size_band": "Medium",
        "peer_count": 15,
        "peer_25th": 58.70,
        "peer_median": 69.90,
        "peer_75th": 81.50,
    },
    {
        # PG-27 test case
        "industry": "Finance",
        "region": "West",
        "size_band": "Small",
        "peer_count": 8,
        "peer_25th": 55.00,
        "peer_median": 63.00,
        "peer_75th": 72.00,
    },
]


async def get_benchmark_aggregate(
    industry: str,
    region: str,
    size_band: str,
):
    for record in BENCHMARK_DATA:
        if (
            record["industry"] == industry
            and record["region"] == region
            and record["size_band"] == size_band
        ):
            return record

    return None