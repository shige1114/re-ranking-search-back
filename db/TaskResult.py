from db import db_session
from db.models import SearchResult,TaskResult,SearchTask,NowVector
from sqlalchemy import select
from typing import List
N = 7


def insert_task_result(task_result: TaskResult):
    # Code to insert task result into the database
    with db_session() as session:
        session.add(task_result)
        session.commit()
    pass

def get_task_result(user_id,session,ids: List[str]) -> List[TaskResult] :
    # Code to retrieve task result from the database
    results = []
    for id in ids:
        query = select(TaskResult).where(TaskResult.search_result_id == id,TaskResult.user_id == user_id)
        results.append(session.execute(query).first()) 
    return [result[0] for result in results]

def get_ideal_vec(user_id,session) -> NowVector:
    
    query = select(NowVector).where(NowVector.user_id == user_id)
    result = session.execute(query).first()
    return result

def update_task_result_by_ids(ids: List[str],session)  :
    try:
        for i,id in enumerate(ids):
            query = select(TaskResult).where(TaskResult.id == id)
            task_result = session.execute(query).first()
            task_result.update_rank(i)
            session.add(task_result)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e

def update_task_result(r,s,ad,session_id,session):
    """
    タスクリザルトの更新
    """
    # r,s,adのtask resultを更新
    # リランキング対象のsearch resultをtaskresultから取得
    
    # sからtaskresultを取得
    all_task_result = get_task_result(session_id,session,s)
    # taskresultを更新
    for task_result in all_task_result:
        if (task_result.search_result_id in r):
            task_result.is_r()
        elif (task_result.search_result_id in ad):
            task_result.is_ad()
        else:
            task_result.is_s()
        session.add(task_result)
        print("update_task_result",task_result.__str__())
    session.commit()
    
def update_re_ranked_task_result(re_ranked_task_result: List[TaskResult],session):
    """
    リランキング済みのタスクリザルトの更新
    """
    try:
        for task_result in re_ranked_task_result:
            session.add(task_result)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e
    
    
    