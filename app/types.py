from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_serializer
from typing import Dict, Any


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class Costs(BaseModel):
    input_token_cost: Decimal
    output_token_cost: Decimal
    input_cost: Decimal
    output_cost: Decimal
    total_cost: Decimal

    class Config:
        json_encoders = {Decimal: lambda v: f"{v:.12f}".rstrip("0").rstrip(".")}


class CallAPIResult(BaseModel):
    model: str
    usage: Usage
    costs: Costs
    result: Dict[str, Any]
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_datetime(self, dt: datetime):
        return dt.isoformat()
