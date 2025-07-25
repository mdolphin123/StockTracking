from typing import Annotated
import httpx
import json
import datetime
from typing import List
import uuid
from typing import Set, Any



#query request from to and store raw data in those time intevals
#storing poll data into raw data and storing configs into the configs
#get request is from PROCESSED data (not raw data)
#If you have a cache miss you store into raw data
#After you store into raw data you immediately try to store into processed data
#What to do on a cache miss
#Use the configs to config the background task

import apscheduler
import os
#from services.producer import producer
import asyncio
from aiokafka import AIOKafkaConsumer
from kafka import TopicPartition


from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker
from apscheduler.triggers.interval import IntervalTrigger
from fastapi.middleware.cors import CORSMiddleware



from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Query, status
#from fastapi_scheduler import SchedulerAdmin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint, Column, JSON
from sqlalchemy import Column, String, DateTime, Float, Index, desc
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import create_async_engine
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from app.models.RawData import RawData
from app.models.ProcessedData import ProcessedData
from app.models.MovingAverage import MovingAverage
from app.models.polling_config import PollingConfig
from app.api.get_price import get_router
from app.api.poll_price import post_router
from app.api.get_average import get_router2
from app.api.get_graph import get_router3
from app.core.database import SessionDep, get_session
from app.core.config import DATABASE_URL2
from app.services.get_average import get_average



#Raw data is just JSON file and some extra metadata
#Function to convert from raw to processed data
#Every time you get raw data you immediately try to convert it into processed data
#Convert from raw data to processed data

#Just for now, to toggle column names



#scheduler = BackgroundScheduler(job_defaults = job_defaults, jobstores=jobstores, timezone='America/New_York') 
scheduler = None
engine = None



loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
    'price-updates-new', loop = loop, group_id = "test_group", bootstrap_servers = 'kafka:9092', auto_offset_reset = 'earliest') #, auto_offset_reset = 'earliest'

async def consume():
    values = {}
    try:
        await asyncio.sleep(10)
        await consumer.start()

        '''
        partitions: Set[TopicPartition] = consumer.assignment()
    
        for tp in partitions:
            end_offset_dict = await consumer.end_offsets([tp])
            end_offset = end_offset_dict[tp]

            print(end_offset)
            consumer.seek(tp, max(0, end_offset-1))
        '''
        
        
     
    except Exception as e:
        print(e)
        return

    try:
        async for message in consumer:
            data = json.loads(message.value)
            symbol = data["symbol"]

            print(symbol)

            price = data["price"]
            timestamp = data["timestamp"]
            get_average(symbol, timestamp, price, values) #what to do abt the sessions...

    finally:
        await consumer.stop()




@asynccontextmanager
async def lifespan(app: FastAPI):
    #scheduler.start()
    global scheduler
    global engine
    engine = create_async_engine(DATABASE_URL2)
    

    data_store = SQLAlchemyDataStore(engine)

    event_broker = AsyncpgEventBroker.from_async_sqla_engine(engine)
    scheduler = apscheduler.AsyncScheduler(data_store, event_broker)


    #for hard resets if needed 
   
    #async with engine.begin() as conn:
        #await conn.run_sync(SQLModel.metadata.create_all)
        #await conn.run_sync(SQLModel.metadata.drop_all)
        #await conn.run_sync(SQLModel.metadata.create_all)

 
    
    async with scheduler:
        await scheduler.start_in_background()
        task = asyncio.create_task(consume())
        yield

        task.cancel()
        consumer.stop()
        
        try:
            await task

        except asyncio.CancelledError:
            print("Consumer Task Cancelled")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(get_router)
app.include_router(get_router2)
app.include_router(get_router3)


