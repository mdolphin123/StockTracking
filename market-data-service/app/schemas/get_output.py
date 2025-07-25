from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
import uuid
from app.schemas.config_schema import config_schema
import pytz
eastern_timezone = pytz.timezone('US/Eastern')


class get_output_schema(BaseModel):
    symbol: str = Field(default = None)
    open: float = Field(default = None)
    timestamp: datetime = Field(default = datetime.now(eastern_timezone))
    provider: str = Field(default = "alpha_vantage")

