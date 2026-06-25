# ============================================================
# schemas.py
# ============================================================

from typing import Dict, List, Any
from pydantic import BaseModel


class FlowRequest(BaseModel):
    features: Dict[str, Any]


class BatchRequest(BaseModel):
    flows: List[Dict[str, Any]]