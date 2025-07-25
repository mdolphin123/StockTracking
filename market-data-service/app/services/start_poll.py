
from app.core.database import SessionDep
import httpx
import datetime

from datetime import datetime

from sqlmodel import select
from sqlalchemy import desc
from app.models.RawData import RawData
from app.services.raw_to_processed import raw_to_processed
from app.core.config import API_KEY
#from app.core.database import SessionDep
from app.core.database import get_session
import pytz
eastern_timezone = pytz.timezone('US/Eastern')

from abc import ABC, abstractmethod



async def start_poll(time_interval: int, symbols: list[str]):    
    print(datetime.now(eastern_timezone))
    URL = "https://www.alphavantage.co/query"
    
    for i in range(0, len(symbols)):
        params = {"function": 'TIME_SERIES_INTRADAY',
              "symbol": symbols[i],
              "interval": "1min",
              "apikey": API_KEY}
        response = httpx.get(URL, params = params, timeout=10.0)

        #getting the most recent response!!
        data = response.json()
        
        gen = get_session()
        session = next(gen)
        
        temp = session.exec(select(RawData).where(RawData.symbol == symbols[i]).order_by(desc(RawData.last_refreshed)).limit(1)).first()
        
        if "Meta Data" in data:
            temp_time = data["Meta Data"]["3. Last Refreshed"]
            refreshed = datetime.strptime(temp_time, '%Y-%m-%d %H:%M:%S')

            if temp == None or refreshed != temp.last_refreshed: #not teh same
                row = RawData(symbol = symbols[i], interval = time_interval, raw_data = data)
                session.add(row)
                session.commit()

                raw_to_processed(row, session, time_interval)
            #store to raw data
        else:
            print("API used up")
            
        gen.close()

'''
async def testing():
    print("hello")
    '''