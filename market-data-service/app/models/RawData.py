import datetime
import uuid
import pytz

from datetime import datetime

from sqlmodel import Field, SQLModel, Column, JSON
from sqlalchemy import Column

eastern_timezone = pytz.timezone('US/Eastern')


class RawData(SQLModel, table=True):
    __table__name__ = "rawdata"

    #Extra metadata stuff
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(default = None, index = True) #get from user, SYMBOL IS INDEX!
    interval: int = Field(default = None)

    from_timestamp: datetime = Field(default = datetime.now(eastern_timezone), index = True)
    to_timestamp: datetime = Field(default = datetime.now(eastern_timezone), index = True)
    created: datetime = Field(default = datetime.now(eastern_timezone), index = True) #Time you got the data!
    raw_data: dict = Field(default_factory = dict, sa_column = Column(JSON)) #The actual raw data in a JSON file

    last_refreshed: datetime = Field(default = datetime.now(eastern_timezone), index = True)


    #Need to have the raw JSON file here

    model_config = {
        "arbitrary_types_allowed": True
    }