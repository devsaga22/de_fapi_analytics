from fastapi import APIRouter,Depends,HTTPException
from ..db.session import get_session
from sqlmodel import Session,select
from .modelsDTO import EventDTO
from .db_models_schemas import EventCreateSchema,EventUpdateSchema,EventListSchema,EventModel, get_utc_now
router = APIRouter()


@router.get("/")
async def get_events():
    return {"message": "List of events"}

@router.get("/events_list",response_model=EventListSchema)
def get_events_list(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(EventModel.created_at.desc()).limit(10) # pagination with offset and params
    events = session.exec(query).all()
    return EventListSchema(events=events, count=len(events))

# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id:int, session: Session = Depends(get_session)):
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result

@router.post("/",response_model=EventDTO)
def create_event(payload: EventCreateSchema, session:Session=Depends(get_session)):
    # here we will add the logic to create an event in the database using the db session
    data= payload.model_dump() #payload->dict-> pydantic model 
    obj=EventModel.model_validate(data) # dict->sqlmodel model
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.put("/{event_id}",response_model=EventUpdateSchema)
def update_event(event_id:int, payload: EventUpdateSchema, session:Session=Depends(get_session)):
    # here we will add the logic to update an event in the database using the db session
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    #payload->dict-> pydantic model, exclude_unset will exclude the fields that are not set in the payload, so we can update only the fields that are set in the payload
    data = payload.model_dump(exclude_unset=True) 
    for key, value in data.items():
        # anyhow the data has no id attr as we set exclude_unset=true and the EventUpdateSchema has no id field,
        # # we don't allow to update the id field 
        if key =='id':
            continue 
        setattr(obj, key, value) # update the fields that are set in the payload
    obj.updated_at = get_utc_now() # update the updated_at field to the current time
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{event_id}")
def delete_event(event_id:int, session:Session=Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(obj)
    session.commit()
    return {"message": "Event deleted successfully"}