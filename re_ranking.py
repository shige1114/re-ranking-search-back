from db.models import SearchResult,TaskResult,SearchTask,NowVector
from db.SearchResult import *
from db.TaskResult import *
from db.now_vector import *
from collections import OrderedDict
from typing import List,Union
import numpy as np
def _sum_vec(vecs:List[SearchResult]):
    """
    ベクトルの合計を計算
    """
    sum_vec = np.zeros(200)
    for vec in vecs:
        sum_vec += vec.to_vec()
    return sum_vec
def _alph(k):
    return 1.0/(k+1)
def _calculation_ideal_vector(r,s,ad,a):
    return r-s+ad*a

def _cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
def create_ideal_vector(r,s,ad,session) -> NowVector:
    """
    理想ベクトルの作成
    """
    #　理想ベクトルをロード
    # R,S,ADからtaskresultを取得

    # r,s,ad,とitemから取得
    # 理想ベクトル算出
    r_vecs = get_search_result_by_id(r,session)
    s_vecs = get_search_result_by_id(s,session)
    ad_vecs = get_search_result_by_id(ad,session)
    now_ideal_vec = _calculation_ideal_vector(_sum_vec(r_vecs),_sum_vec(s_vecs),_sum_vec(ad_vecs),_alph(len(s)))
    
    return now_ideal_vec


def determining_target_re__ranking(r,s,ad,session_id,session) -> List[Union[SearchResult, TaskResult]]:
    update_task_result(r,s,ad,session_id,session)
    return get_target_task_result(session_id,session)

def _re_rank(ideal_vec, target_re_ranking: List[Union[SearchResult, TaskResult]]) -> List[TaskResult]:
    """
    リランキングを開始
    """
    # 類似度計算
    # 未提示データをリランキング
    tmp = []
    print('-------')
    print(target_re_ranking[0])
    if len(target_re_ranking) == 0 :
        return []
    highest = target_re_ranking[0][0].rank  # 修正: リストの最初の要素のrankメソッドを呼び出す
    for target in target_re_ranking:
        print(target)
        tmp.append([_cos_sim(ideal_vec, target[0].to_vec()),target[1]])
    sorted_tmp = sorted(tmp, key=lambda x: x[0], reverse=True)
    for i, key in enumerate(sorted_tmp):
        key[1].re_rank(highest + i)
        key[1].update()
    # 修正: キーと値のリストを返す
    print(sorted_tmp)
    return list(x[1] for x in sorted_tmp) 
    
    
def re_rank(r,s,ad,session_id) -> List[SearchResult]:
    """
    リランキング
    """
    with db_session() as session:
        # 理想ベクトルの作成
        ideal_vec = create_ideal_vector(r,s,ad,session)
        # リランキング対象の決定
        target_re_ranking = determining_target_re__ranking(r,s,ad,session_id,session)
        print("target_re_ranking:",target_re_ranking)
        result_re_ranking = _re_rank(ideal_vec,target_re_ranking)
        update_re_ranked_task_result(result_re_ranking,session)
        # result_re_ranking = get_search_result_by_id(result_re_ranking_ids,session)
        # update_task_result_by_ids(result_re_ranking_ids,session)