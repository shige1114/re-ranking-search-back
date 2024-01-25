
import pandas as pd
from db import db_session
from db.models import SearchResult,SearchTask
from sqlalchemy.orm import declarative_base, Session

import uuid

from db.models import main
main()

smart_file_path = '/back/db/initialize/スマートフォン.xlsx'
english_file_path = '/back/db/initialize/英会話教材.xlsx'
sdf = pd.read_excel(smart_file_path)
edf = pd.read_excel(english_file_path)

with db_session() as session:
    smart_task = SearchTask(id=str(uuid.uuid4()),name='スマートフォン')
    english_task = SearchTask(id=str(uuid.uuid4()),name='英会話教材')
    session.add(smart_task)
    session.add(english_task)
    session.commit()

    for index, row in sdf.iterrows():
        print(row['ad'])
        if (row['ad'] == True):
        
            ad = True
        else:
            ad = False
        search_result = SearchResult(
            id=str(uuid.uuid4()),
            rank=row['no'],
            title=row['title'],
            snippet=row['snippet'],
            url=row['link'],
            window_url=row['display_link'],  # Assuming 1 represents True, 0 represents False
            vector=row['vector'],
            is_ad = ad,# Assuming 'vector' is a column in your DataFrame
            # Assuming 'search_task_id' is a column in your DataFrame
            search_task_id=smart_task.id
        )
        session.add(search_result)
    
    for index, row in edf.iterrows():

        search_result = SearchResult(
            id=str(uuid.uuid4()),
            rank=row['no'],
            title=row['title'],
            snippet=row['snippet'],
            url=row['link'],
            window_url=row['display_link'],  # Assuming 1 represents True, 0 represents False
            vector=row['vector'],  # Assuming 'vector' is a column in your DataFrame
            is_ad=ad,
            # Assuming 'search_task_id' is a column in your DataFrame
            search_task_id=english_task.id
        )
        session.add(search_result)
    session.commit()


    