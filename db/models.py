from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from db import engine
import json
import numpy as np

Base = declarative_base()

class SearchResult(Base):
    __tablename__ = 'search_results'
    id = Column(String, primary_key=True, index=True)
    rank = Column(Integer)
    title = Column(String, index=True)
    snippet = Column(String)
    url = Column(String, index=True)
    window_url = Column(String)
    is_ad = Column(Boolean ,default=False)
    vector = Column(String)
    search_task_id = Column(String, ForeignKey('search_tasks.id'))
    
    def to_vec(self):
        return np.array(json.loads(self.vector))

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    task_id = Column(String, ForeignKey('search_tasks.id'))

class SearchTask(Base):
    __tablename__ = 'search_tasks'
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
class TaskResult(Base):
    __tablename__ = 'task_results'

    user_id = Column(String, ForeignKey('users.id'))
    search_result_id = Column(String, ForeignKey('search_results.id'))
    
    now_rank = Column(Integer)
    history_rank = Column(String, default='[]')  # 'prompt' or 'browse'
    
    is_view = Column(Boolean, default=False)
    is_click = Column(Boolean, default=False)
    
    ad = Column(Boolean, default=False)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'search_result_id'),
    )

    def is_s(self):
        self.is_view = True
    
    def is_r(self):
        self.is_click = True
        self.is_view = True
    
    def is_ad(self):
        self.ad = True
        self.is_view = True
        self.is_click = True
    
    def re_rank(self, rank):
        tmp = json.loads(self.history_rank)
        tmp.append(self.now_rank)
        self.history_rank = json.dumps(tmp)
        self.now_rank = rank
    
    def update(self):
        self.timestamp = func.now()
    def __str__(self):
        return f"<TaskResult(user_id={self.user_id}, search_result_id={self.search_result_id}, now_rank={self.now_rank}, " \
               f"history_rank={self.history_rank}, is_view={self.is_view}, is_click={self.is_click}, ad={self.ad}, " \
               f"timestamp={self.timestamp})>"
        
    

class NowVector(Base):
    __tablename__ = 'now_vectors'

    user_id = Column(String, ForeignKey('users.id'),primary_key=True)
    vector = Column(String)
    def to_vec(self):
        return np.array(json.loads(self.vector))
    def to_string(self,vector):
        self.vector = np.array2string(vector, separator=',')
        
    def update_vector(self,vector):
        self.vector = np.array2string(vector, separator=',')
        """
        python -m db.models
        """
def main():
    print("db作成開始")
    Base.metadata.create_all(bind=engine)
