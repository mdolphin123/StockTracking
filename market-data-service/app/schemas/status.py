import uuid
from sqlmodel import Field, SQLModel, Column, JSON
from sqlalchemy import Column, DateTime
from pydantic import BaseModel
from datetime import datetime
import enum


class polling_config_status(str, enum.Enum):
    accepted = "accepted"
    duplicate = "duplicate"
    rejected = "rejected"

    
