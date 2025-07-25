from pydantic import BaseModel
from sqlmodel import SQLModel, Field, DateTime, Column, JSON
from datetime import datetime
import uuid
from app.schemas.config_schema import config_schema
from app.schemas.status import polling_config_status


class poll_output_schema(BaseModel):
    job_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: polling_config_status = Field(default = None)
    config: config_schema = Field(default = None)


