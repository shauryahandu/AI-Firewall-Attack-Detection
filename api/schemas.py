from typing import Dict, List
from pydantic import BaseModel


class FlowRequest(BaseModel):
    features: Dict[str, float]


class BatchRequest(BaseModel):
    flows: List[FlowRequest]