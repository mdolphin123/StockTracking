from typing import Annotated
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends

from app.core.config import DATABASE_URL
from app.models.RawData import RawData
from app.models.ProcessedData import ProcessedData
from app.models.MovingAverage import MovingAverage
from app.models.polling_config import PollingConfig


#connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL) #connect_args=connect_args)

#RawData.metadata.drop_all(bind=engine)
#RawData.metadata.create_all(bind=engine)



def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

