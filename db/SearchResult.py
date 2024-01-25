from db import db_session
from db.models import SearchResult,SearchTask,TaskResult
from sqlalchemy import select
from typing import List,Union
from sqlalchemy.orm.exc import NoResultFound
Num = 7
N = 7
def _sum_list(list1,list2):
    result = [None]* (len(list1)+len(list2))
    print("len(list1):",len(list1))
    print("len(list2):",len(list2))
    n = len(list1)//len(list2)
    print("n:",n)
    if (len(list2) == 1):
        tmp = 2
    else:
        tmp = len(list2)
    for i in range(len(result)):
        if i % n == 0:
            t = i//n
            print(t)
            result[i] = list2[t//tmp]
            
        else:
            # print("i:",i)
            # print("t:",t)
            # print("i-t:",i-t)
            
            result[i] = list1[i-t-1]
    # print(result)
    print(result)
    return result
def get_search_result(task_name: str, offset: int, user_id: str):
    # Code to retrieve search result from the database
    with db_session() as session:
        query = select(SearchResult).join(TaskResult,SearchResult.id == TaskResult.search_result_id)\
        .where(TaskResult.now_rank <= offset,TaskResult.user_id == user_id,TaskResult.ad ==False)\
                .order_by(TaskResult.now_rank)
        results = session.execute(query).all()
        print("get_search_result:result num",len(results))
        print("------------------>>")
        print(len(results))
        print(len(results)//N)
        if (len(results)//N == 0):
            limit = 1
        else:
            limit = len(results)//N
        query = select(SearchResult).join(TaskResult,SearchResult.id == TaskResult.search_result_id)\
            .where(TaskResult.now_rank <= offset,TaskResult.user_id == user_id,SearchResult.is_ad == True)\
                .order_by(TaskResult.now_rank)\
                .limit(limit)
        result2s = session.execute(query).all()
    list_resutls = [result[0] for result in results]
    list_result2s = [result2[0] for result2 in result2s]

    return _sum_list(list_resutls,list_result2s)

    

def delete_search_result(search_result_id: int):
    # Code to delete search result from the database

    pass

# def _get_search_result_num(rank:int,query:str):
#     return select(SearchResult).where(
#         SearchResult.rank.between(rank,rank+N),
#         SearchResult.search_task_id.in_(select(SearchTask.id
#     ).where(SearchTask.name == query)))


def get_search_result_by_id(ids: List[str],session) :
    # Code to retrieve search result from the database
    results = []        
    for id in ids:
        query = select(SearchResult).where(SearchResult.id == id)
        results.append(session.execute(query).first())
    
    print(results)
    return [result[0] for result in results]


# def get_result_to_rerank(ids: List[str],query:str):
#     # Code to retrieve search result from the database
#     results = {}
#     with db_session() as session:
#         for id in ids:
#             query = select(SearchResult).where(SearchResult.id == id)
#             results[id] = session.execute(query).first()
#         new_result = list(results.values())[-1]
#         yet_results = session.execute(_get_search_result_num(new_result.rank,query)).fetchall()
#     return results,yet_results


def get_target_task_result(user_id,session) -> List[Union[SearchResult,TaskResult]]:
    # Code to retrieve task result from the database
    query = select(SearchResult,TaskResult).join(TaskResult,SearchResult.id == TaskResult.search_result_id)\
        .where(TaskResult.user_id == user_id,TaskResult.ad == False,TaskResult.is_view == False)\
        .order_by(TaskResult.now_rank)\
                .limit(Num)
        # .where(TaskResult.is_ad == False,TaskResult.is_view == False)\
    
    results = session.execute(query).all()
    print("---------------------------------",results[0][1].__str__())
    return results