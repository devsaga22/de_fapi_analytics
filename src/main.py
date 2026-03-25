from fastapi import FastAPI
from .api.events.routing import router as events_router
from contextlib import asynccontextmanager

from .api.db.session import init_db

""" need init configs before just like ioc container in java spring, but here we can just call the init function to do the job, no need to use decorator or something else to mark it as a init function, just call it before the app starts to run, and it will do the job, and we can also call it multiple times if we want to re-init the configs, but in this case we just call it once at the start of the app."""
@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db connection
    init_db()
    yield
    # close db connection

app = FastAPI(lifespan=lifespan)
app.include_router(events_router,prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "Worlders"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def read_app_health():
    return {"status": "healthy"}