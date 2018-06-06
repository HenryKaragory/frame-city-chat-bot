from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class Customer(Base):
	__tablename__ = 'CustomerInformation'

	first_name = Column('FirstName', String(50))
	last_name = Column('LastName', String(50))
	email = Column('Email', String(75))
	address = Column('Address', String(100))
	phone = Column('Phone', String(22))
	psid = Column('Psid', Integer, primary_key=True)

	messages = relationship("Message", back_populates="customer")
	ratings = relationship("Rating", back_populates="customer")

class Message(Base):
	__tablename__ = 'Messages'

	received_message = Column('ReceivedMessage',String(1000), nullable=False)
	sent_message = Column('SentMessage', String(255), nullable=False)
	entity = Column('Entity', String(50), nullable=False)
	value = Column('Value', String(50))
	created = Column('Created', DateTime, nullable=False)
	id = Column('id', Integer, primary_key=True)
	psid = Column('Psid', Integer, ForeignKey('CustomerInformation.Psid'))
	customer = relationship("Customer", back_populates="messages")

class Rating(Base):
	__tablename__ = 'Ratings'

	id = Column('id', Integer, primary_key=True)
	psid = Column('Psid', Integer, ForeignKey('CustomerInformation.Psid'))
	rating = Column('Rating', Integer, nullable=False)
	comment = Column('Comment', String(255), nullable=True)

	customer = relationship("Customer", back_populates="ratings")

class AskExperienceCountDown(Base):
	__tablename__ = 'AskExperienceCountDown'

	psid = Column('Psid', Integer, primary_key=True, nullable=False)
	count = Column('Count', Integer, nullable=False)


