from fastapi import APIRouter, Query
from typing import Annotated
import httpx
import json
from typing import List
import uuid

from datetime import datetime
from app.core.database import SessionDep
from app.models.MovingAverage import MovingAverage

from typing import Annotated
import httpx
import json
import datetime
from typing import List
import uuid


from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint, Column, JSON
from app.schemas.get_output import get_output_schema
from app.core.config import API_KEY
from sqlalchemy import Column, String, DateTime, Float, Index, desc
from pydantic import BaseModel

get_router2 = APIRouter()

@get_router2.get("/average")
#dont need session: SessionDep, bc you arent actually storing anything here (that is for the other functions!)
def read_rows(session: SessionDep, symbol: str = Query()):
    #for testing!!!!

    statement = select(MovingAverage).where(MovingAverage.symbol == symbol)
    item = session.exec(statement).first()

    #if cache miss, get it from the data provider, then add it into the DB
    #WHAT defines Cache miss? Like not the latest? Or just not there?? Like what
    if item is None:
        return {"Detail: Nothing for this symbol yet!"}
    else:
        print("else")
        price = item.moving_average
        timestamp = item.latest_timestamp
    

    return {
        "price": price,
        "timestamp": timestamp
    }