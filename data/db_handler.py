# data/db_handler.py
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, Float
from sqlalchemy.sql import insert, select


DB_PATH = os.environ.get('AI_SIM_DB', 'sqlite:///ai_simulations.db')
engine = create_engine(DB_PATH, echo=False)
metadata = MetaData()


user_actions = Table(
    'user_actions', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', String, nullable=False),
    Column('scenario_id', String, nullable=False),
    Column('payload', JSON),
)


def init_db():
    metadata.create_all(engine)


def save_user_action(user_id: str, scenario_id: str, payload: dict):
    with engine.connect() as conn:
        stmt = insert(user_actions).values(user_id=user_id, scenario_id=scenario_id, payload=payload)
        conn.execute(stmt)


def fetch_actions_for_user(user_id: str):
    with engine.connect() as conn:
        stmt = select([user_actions]).where(user_actions.c.user_id == user_id)
        res = conn.execute(stmt).fetchall()
        return [dict(r) for r in res]