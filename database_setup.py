# SQLALCHEMY IMPORTS
from sqlalchemy import Column, ForeignKey, Integer, String, \
                       DATETIME, func, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key = True)
  username = Column(String(250))
  email = Column(String(250))
  picture = Column(String(250), default = "http://placehold.it/250x250")
  desc = Column(String(250))
  goal = relationship('Goal', backref='author')
  comments = relationship('Comments', backref='author')

  @property
  def serialize(self):
   """Return object data in easily serializeable format"""
   return {
       'id': self.id,
       'username': self.username,
       'email': self.email,
       'picture': self.picture,
       'description': self.description
   }
  
 
class Goal(Base):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    timestamp = Column(TIMESTAMP, default = func.current_timestamp())
    picture = Column(String(250), default = "http://placehold.it/250x250")
    description = Column(String(250))
    isDone = Column(Integer)
    isPrivate = Column(Integer)
    user_id = Column(Integer,ForeignKey('user.id'))
    comments = relationship('Comments', backref='goal', cascade="all, delete-orphan")


    @property
    def serialize(self):
     """Return object data in easily serializeable format"""
     return {
         'title' : self.title,
         'description' : self.description,
         'timestamp'  : str(self.timestamp),
         'picture'  : self.picture,
         'id': self.id,
         'user_id': self.user_id,
         'completed': self.isDone,
         'private': self.isPrivate
     }

class Comments(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True)
  content = Column(String(500), nullable = False)
  timestamp = Column(TIMESTAMP, default = func.current_timestamp())
  user_id = Column(Integer, ForeignKey('user.id'))
  goal_id = Column(Integer, ForeignKey('goal.id'))


  @property
  def serialize(self):
     """Return object data in easily serializeable format"""
     return {
         'id': self.id,
         'content': self.content,
         'timestamp': str(self.timestamp)
     }


engine = create_engine('postgres://iigxfodmrbheti:-RE8qLKecB78W5RQs98aeqvp7M@ec2-107-21-221-59.compute-1.amazonaws.com:5432/dfmhginorv44q4')
 

Base.metadata.create_all(engine)
