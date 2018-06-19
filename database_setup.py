import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Importing is done

Base = declarative_base()


class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   name = Column(String(250), nullable=False)
   email = Column(String(250), nullable=False)
   picture = Column(String(250))


class Club(Base):
    __tablename__ = 'club'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class TeamPlayer(Base):
    __tablename__ = 'team_player'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    club_id = Column(Integer, ForeignKey('club.id'))
    club = relationship(Club)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


# Database is created after running this file
engine = create_engine('sqlite:///footballclubs.db')


Base.metadata.create_all(engine)

