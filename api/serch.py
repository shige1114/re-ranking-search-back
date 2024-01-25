from fastapi import APIRouter,Cookie
from typing import Union,List
from pydantic import BaseModel, Field
from db.models import SearchResult
from db.SearchResult import get_search_result
router = APIRouter()


# Pydanticモデル
class SearchResultResponse(BaseModel):
    id: str
    title: str
    snippet: str
    url: str
    window_url: str
    is_ad: bool
    search_task_id: str

def search_result_to_response(search_result: SearchResult):
    return SearchResultResponse(
        id=search_result.id,
        title=search_result.title,
        snippet=search_result.snippet,
        url=search_result.url,
        window_url=search_result.window_url,
        is_ad=search_result.is_ad,
        search_task_id=search_result.search_task_id
    )
def search_results_to_responses(search_results):

    return [search_result_to_response(result) for result in search_results]

@router.get("/search/")
def search(query: str,offset:int,session_id:str):
    # Perform search logic here
    # 検索結果を返す
    results = get_search_result(query,offset,session_id)
    print(session_id)
    print("offset",offset)
    print(len(results))
    search_results = search_results_to_responses(results)
    return {"data":search_results}