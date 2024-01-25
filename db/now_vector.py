from db import db_session
from db.models import NowVector
from sqlalchemy import select
from typing import List



def insert_now_vector(now_vector: NowVector,session):
    # Code to insert now_vector into the database
    session.add(now_vector)
    session.commit()
    pass

def get_now_vector(user_id,session) -> NowVector:
    
    query = select(NowVector).where(NowVector.user_id == user_id)
    result = session.execute(query).first()
    return result