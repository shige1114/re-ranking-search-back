from db.models import User,SearchTask,NowVector,TaskResult,SearchResult
import numpy as np
from db import db_session
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
def insert_user(user_id: str, name: str,query:str,session):
    # Code to insert user into the database
    try:
        query = select(SearchTask.id).where(SearchTask.name == query)
        task_id = session.execute(query).scalar()
        if task_id is None:
            raise NoResultFound
        user = User(id=user_id,name=name,task_id=task_id)
        session.add(user)
        session.commit()
    except NoResultFound:
        print("NoResultFound")
        session.rollback()
        raise NoResultFound
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e
    pass

def delete_user(user_id: str):
    # Code to delete user from the database
    with db_session() as session:
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
    pass

def get_user(session_id: str):
    # Code to retrieve user from the database
    with db_session() as session:
        query = select(User).where(User.id == session_id)
        user = session.execute(query).first()
    return user

def insert_now_vector(session_id: str,session):
    # Code to insert now_vector into the database

    try:
        now_vector = NowVector(user_id=session_id,vector=np.array2string(np.zeros(200),separator=',') )
        session.add(now_vector)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e
    pass


def insert_task_result(session_id: str,task_name: str,session):
    # Code to insert task result into the database
    try:
        query = select(SearchResult.id,SearchResult.rank,SearchResult.is_ad).where(SearchResult.search_task_id.in_(select(SearchTask.id).where(SearchTask.name == task_name)))
        for result in session.execute(query).all():
            task_result = TaskResult(user_id=session_id,search_result_id=result[0],now_rank=result[1],ad=result[2])
            session.add(task_result)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e
    pass


def start_task(session_id: str,user_name:str,task_name:str):
    with db_session() as session:
        try:
            insert_user(session_id,user_name,task_name,session)
            insert_task_result(session_id,task_name,session)
            insert_now_vector(session_id,session)
        except Exception as e:
            print(f"Error: {e}")
            raise e
            
            