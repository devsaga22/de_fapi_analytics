from pydantic import BaseModel

class EventDTO(BaseModel):
    id:int
    name:str
    description:str

