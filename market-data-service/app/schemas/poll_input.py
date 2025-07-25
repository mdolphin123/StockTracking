from typing import List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, DateTime, Column, JSON
from datetime import datetime
import uuid

class poll_input_schema(BaseModel):
    symbols: List[str] = Field(default = None, sa_column=Column(JSON)) #get from user
    interval: int = Field(default = 60)
    provider: str = Field(default = "Alpha Vantage")
