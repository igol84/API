from fastapi import FastAPI
from . import tables
from .database import engine
from .routers import router

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
