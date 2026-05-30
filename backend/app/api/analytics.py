"""Admission analytics endpoint.

Returns aggregate admission metrics. This scaffold serves illustrative sample
data; wire it to your warehouse / DB query when available.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.models.response_models import AdmissionMetric, AnalyticsResponse
from app.services.auth import get_current_user

router = APIRouter(tags=["analytics"])


# Placeholder data — replace with a real query against your data source.
_SAMPLE_METRICS = [
    AdmissionMetric(program="B.Tech CSE", applications=1200, admitted=300, conversion_rate=0.25),
    AdmissionMetric(program="MBA", applications=800, admitted=160, conversion_rate=0.20),
    AdmissionMetric(program="B.Com", applications=950, admitted=380, conversion_rate=0.40),
    AdmissionMetric(program="LLB", applications=420, admitted=126, conversion_rate=0.30),
]


@router.get("/analytics/admissions", response_model=AnalyticsResponse)
async def admission_analytics(
    user: dict[str, Any] = Depends(get_current_user),
) -> AnalyticsResponse:
    total_apps = sum(m.applications for m in _SAMPLE_METRICS)
    total_admitted = sum(m.admitted for m in _SAMPLE_METRICS)
    return AnalyticsResponse(
        total_applications=total_apps,
        total_admitted=total_admitted,
        metrics=_SAMPLE_METRICS,
    )
