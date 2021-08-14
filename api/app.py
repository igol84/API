from fastapi import FastAPI
from . import tables
from .database import engine, add_user_if_empty
from .routers import router

tables.Base.metadata.create_all(bind=engine)
add_user_if_empty()

app = FastAPI()
app.include_router(router)
