from fastapi import APIRouter, Query, Response
from typing import Annotated
import httpx
import json
from typing import List
import uuid
import matplotlib.pyplot as plt
import io


from datetime import datetime
from app.core.database import SessionDep
from app.models.MovingAverage import MovingAverage
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
from datetime import datetime, timedelta
from io import BytesIO
import pytz
from sqlalchemy.sql import text



eastern_timezone = pytz.timezone('US/Eastern')

get_router3 = APIRouter()

@get_router3.get("/graph")
#dont need session: SessionDep, bc you arent actually storing anything here (that is for the other functions!)
def read_rows(session: SessionDep, symbol: str = Query()):
    #for testing!!!!
    five_days = datetime.now(eastern_timezone) - timedelta(days = 5)
    
    query = text("""SELECT DISTINCT ON (DATE(time_stamp)) DATE(time_stamp) AS time_stamp, 
               open
        FROM processeddata
        WHERE symbol = :symbol 
        AND time_stamp >= :start_date
        ORDER BY DATE(time_stamp), time_stamp ASC
        LIMIT 5
    """)

    rows = session.exec(query.params(symbol=symbol, start_date=five_days)).all()

    #if cache miss, get it from the data provider, then add it into the DB
    #WHAT defines Cache miss? Like not the latest? Or just not there?? Like what
    if not rows:
        print("here")
        return {"Detail": "Nothing found"}
    else:
        dates = [row.time_stamp for row in rows]
        prices = [row.open for row in rows]

        print(len(dates))


        fig, ax = plt.subplots(constrained_layout=True)
        ax.plot(dates, prices, marker='o')

        plt.xlabel("Day")
        plt.ylabel("Opening Price")
        plt.title("Opening Price in Past 5 days")
        plt.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(content=buf.read(), media_type="image/png")


