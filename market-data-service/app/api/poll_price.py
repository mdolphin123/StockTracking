from typing import Annotated
import json
from fastapi import APIRouter, Query, Request
from datetime import datetime

from app.core.database import SessionDep
from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint, Column, JSON
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler import ConflictPolicy


from fastapi import BackgroundTasks, status
from app.models.polling_config import PollingConfig
from app.schemas.poll_input import poll_input_schema
from app.schemas.poll_output import poll_output_schema
from app.schemas.config_schema import config_schema
from app.schemas.status import polling_config_status
from app.services.start_poll import start_poll # testing
import pytz


post_router = APIRouter()

eastern_timezone = pytz.timezone('US/Eastern')

#need to get the raw pdates and publish them to topic: get the last 5 prices first!

@post_router.post("/prices/poll",  status_code=status.HTTP_202_ACCEPTED, response_model = poll_output_schema)
async def get_poll(session: SessionDep, item: poll_input_schema):
    from app.main import scheduler
 
    
    time_interval = item.interval #This is NOT the same as interval you pass into params, that is always 1 min
    symbol_list = item.symbols

    #Store the config into polling config!
    row = PollingConfig(job_id = "idk", symbols = symbol_list, interval = time_interval)
    session.add(row)
    session.commit()
    

    #scheduling
    temp = IntervalTrigger(seconds = time_interval, start_time = datetime.now(eastern_timezone))
    await scheduler.add_schedule(start_poll, temp, args = [time_interval, symbol_list], conflict_policy = "replace", id="current")

    #make a config for the output
    myconfig = config_schema(symbols = symbol_list, interval = time_interval)

    #returning the schema
    return poll_output_schema(job_id = row.id, status = polling_config_status.accepted, config=myconfig)

