from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import tables
from .database import engine, add_user_if_empty
from .routers import router

tables.Base.metadata.create_all(bind=engine)
add_user_if_empty()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello!!!"}


app.include_router(router)
