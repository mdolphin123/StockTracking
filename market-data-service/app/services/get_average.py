
from app.models.RawData import RawData
from app.models.ProcessedData import ProcessedData
from app.models.MovingAverage import MovingAverage
from app.models.polling_config import PollingConfig
from app.api.get_price import get_router
from app.api.poll_price import post_router
from app.core.database import SessionDep, get_session

from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint, Column, JSON
from sqlalchemy import desc


from datetime import datetime

#global dictionary what do i do?
#map symbols to 5 prices

def get_average(symbol: str, timestamp: str, price: float, values: dict):    
    gen = get_session()
    session = next(gen)

    #import pdb; pdb.set_trace()
    if symbol not in values or len(values[symbol]) == 0:
        time_stamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

                #I need to sort this and find the value with time, then find the last five...
        temp = session.exec(select(ProcessedData).where(ProcessedData.symbol == symbol).where(ProcessedData.time_stamp <= time_stamp).order_by(desc(ProcessedData.time_stamp)).limit(5))
                
        if symbol not in values:
            values[symbol] = []
                
            #start doing the sum stuff
            sum = 0
            for i in temp: 
                values[symbol].append(i.open)
                sum = sum + i.open #add to sum!
                
            avg = sum/len(values[symbol])

            print("getting average...")


            row = MovingAverage(symbol = symbol, moving_average = avg, latest_timestamp = time_stamp)
            
        else:
            if(len(values[symbol] >= 5)):
                values[symbol] = values[symbol][1:]
            #if length is less than 5, do not cut it
            values[symbol].append(price)
                
            sum = 0
            for i in range(0, len(values[symbol])):
                sum += values[symbol][i]

            avg = sum/len(values[symbol])
            row = MovingAverage(symbol = symbol, moving_average = avg, latest_timestamp = time_stamp)
            
        session.add(row)
        session.commit()