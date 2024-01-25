
from fastapi import APIRouter, Cookie,HTTPException
import uuid
from datetime import datetime, timedelta
from typing import Union
from db.Users import start_task
from pydantic import BaseModel
router = APIRouter()

def generate_session_id(username: str) -> str:
    session_id = str(uuid.uuid4())
    return str(session_id)
    
class Login(BaseModel):
    username: str
    query:str
    
@router.post("/login/")
def login( item:Login):
    # ログイン処理を実装する
    username = item.username
    query = item.query
    session_id = generate_session_id(username)
    try:
        start_task(session_id,username,query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "ログイン成功","data":session_id}