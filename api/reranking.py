
from fastapi import APIRouter, Cookie
import uuid
from datetime import datetime, timedelta
from db.Users import insert_user
from typing import Union,List
from pydantic import BaseModel
from re_ranking import re_rank
from db import db_session

from db.SearchResult import get_search_result_by_id
router = APIRouter()
class Item(BaseModel):
    r: List[str]
    s: List[str]
    ad: List[str]
    session_id: str



    

@router.post("/rerank/")
def rerank(item:Item):
    """
    表示するリランキング結果を作成
    """   
    # Re-rankロジック
    re_ranked_result = re_rank(item.r,item.s,item.ad,item.session_id)
    # taskの更新
    # 返す検索結果を取得
    return {"data":re_ranked_result,"message":"リランキング成功"}
