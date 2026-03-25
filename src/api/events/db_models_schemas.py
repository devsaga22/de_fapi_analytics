from sqlmodel import SQLModel,Field
from typing import Optional,List
from datetime import datetime,timezone
# import sqlmodel
from sqlalchemy import DateTime, Column
from timescaledb import TimescaleModel
# from timescaledb.utils import get_utc_now

def get_utc_now():
    # ignore the timezone of the server follow the utc/gmt time 
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)    

# the entity that will be stored in the database--
#  only postgres -- use SQLModel
# timeseries db-- use the timescaleModel
# page visits at any given time

class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True) # /about, /contact, # pricing
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
# the return type of the get all events api
class EventListSchema(SQLModel):
    events: List[EventModel]
    count: int

class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int