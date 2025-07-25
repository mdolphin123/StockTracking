import uuid
from sqlmodel import Field, SQLModel

class MovingAverage(SQLModel, table=True):
    __table__name__ = "moving averages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(index=True) #get from user, idk what the primary key should even be here tbh
    moving_average: float = Field()
    latest_timestamp: str = Field(index = True) #idk if i should switch this to datetime, ALSO INDEX!
    #oldest_price: float = Field(default = None)

    model_config = {
        "arbitrary_types_allowed": True
    }
