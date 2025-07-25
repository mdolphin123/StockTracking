from datetime import datetime
import uuid
import pytz
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

eastern_timezone = pytz.timezone('US/Eastern')


class ProcessedData(SQLModel, table=True):
    __table__name__ = "Processed Data"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(index=True) #get from user, SYMBOL IS INDEX!

    created: datetime = Field(default = datetime.now(eastern_timezone), index = True) #idk if i should switch this to datetime, ALSO INDEX!
    time_stamp: datetime = Field(default = datetime.now(eastern_timezone), index = True)

    #from timestamp, to timestamp, and interval
    #response is JSON datam,
    interval: int = Field(default=None) #also get from user
    open: float = Field(default=None)
    close: float = Field(default=None) 
    high: float = Field(default=None) 
    low: float = Field(default=None) 

    model_config = {
        "arbitrary_types_allowed": True
    }

    __table_args__ = (
        UniqueConstraint("symbol", "time_stamp"),
    )


    #get the raw data as a JSON file and put it into processed data!