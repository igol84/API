from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .hashing import Hash
from .settings import settings
from . import tables

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_user_if_empty():
    db = SessionLocal()
    user: tables.User = db.query(tables.User).first()
    if not user:
        new_store = tables.Store(name='shop', desc='')
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        new_seller = tables.Seller(store_id=new_store.id, name='Igor')
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        new_user = tables.User(id=new_seller.id, email='qwe', password=Hash.bvcrypt('qwe'), role='admin')
        db.add(new_user)
        db.commit()

    db.close()
