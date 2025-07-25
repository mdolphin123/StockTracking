from typing import List
import uuid
from sqlmodel import Field, SQLModel, Column, JSON
from pydantic import BaseModel


class PollingConfig(SQLModel, table = True): 
    #arbitrary_types_allowed = True
    
    job_id: str = Field(default = None) #job id
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbols: List[str] = Field(default = None, sa_column=Column(JSON)) #get from user
    interval: int = Field(default=None, index=True)
    #need another field for provider, but ignore this rn

    model_config = {
        "arbitrary_types_allowed": True
    }
