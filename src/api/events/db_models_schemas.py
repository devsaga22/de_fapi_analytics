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
class EventModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(default_factory=get_utc_now,
                                sa_type=DateTime(timezone=True),
                                nullable=False)
    updated_at: datetime = Field(default_factory=get_utc_now,
                                sa_type=DateTime(timezone=True),
                                nullable=False)




class EventCreateSchema(SQLModel):
    name: str
    description: Optional[str] = Field(default="")
# we allow only description to be updated for now, DTO
class EventUpdateSchema(SQLModel):
    # name: Optional[str] = None
    description: Optional[str] = None
# the return type of the get all events api
class EventListSchema(SQLModel):
    events: List[EventModel]
    count: int