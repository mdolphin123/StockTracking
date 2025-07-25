from fastapi import APIRouter, Query
from typing import Annotated
import httpx
import json
from typing import List
import uuid

from datetime import datetime
from app.core.database import SessionDep
from app.models.ProcessedData import ProcessedData

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

get_router = APIRouter()

@get_router.get("/prices/latest", response_model = get_output_schema)
#dont need session: SessionDep, bc you arent actually storing anything here (that is for the other functions!)
def read_rows(session: SessionDep, symbol: str = Query()):
    #for testing!!!!

    statement = select(ProcessedData).where(ProcessedData.symbol == symbol).order_by(desc(ProcessedData.time_stamp))
    item = session.exec(statement).first()

    #if cache miss, get it from the data provider, then add it into the DB
    #WHAT defines Cache miss? Like not the latest? Or just not there?? Like what
    if item is None:
        print("add")
        URL = "https://www.alphavantage.co/query"
        params = {"function": 'TIME_SERIES_INTRADAY',
                  "symbol": symbol,
                  "interval": "1min",
                  "apikey": API_KEY}
        response = httpx.get(URL, params = params)
        data = response.json()
        time_series = data["Time Series (1min)"]

        timestamp = list(time_series.keys())[-1]
        open = float(time_series[timestamp]["1. open"]) 
        close = float(time_series[timestamp]["4. close"]) 
        high = float(time_series[timestamp]["2. high"]) 
        low = float(time_series[timestamp]["3. low"]) 
        #Also think I need to sort this by datetime
        
        #now must store this into raw data now...!! Note we have already retrieved the session! What do I put as interval...
        row = ProcessedData(symbol = symbol, time_stamp=timestamp, interval = 60, open = open, close = close, high = high, low = low) #for now
        price = row.open
        session.add(row)
        session.commit()

        return get_output_schema(symbol = symbol, open = price, timestamp = timestamp, provider = "alpha_vantage")
    else:
        print("else")
        price = item.open
        timestamp = item.time_stamp

        return get_output_schema(symbol = symbol, open = price, timestamp = timestamp, provider = "alpha_vantage")
