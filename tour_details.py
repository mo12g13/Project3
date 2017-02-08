from sqlalchemy import Table, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import DATE, DATETIME
from base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import event
from sqlalchemy.engine import Engine
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
engine = create_engine('sqlite:///game_tour.db', echo=True)
Base = declarative_base()


class Game(Base):
    """A table that holds the schedule for each game"""
    __tablename__='game_schedule'
    venue_id = Column(Integer(), primary_key=True)
    stadium = Column(String(50), nullable=False)
    game_location =Column(String(50), nullable=False)
    game_date = Column(String(50), default=datetime.now().strftime("%d/%m/%y"))
    date_updated = Column(DATETIME(), default=datetime.now)

    def __str__(self):
        game_record='Game details: venue_id={} stadium={} game_location={} game_date={} date_updated={}'
        return game_record.format(self.venue_id, self.stadium, self.game_location, self.game_date, self.date_updated)


class Merchandise(Base):
    """A table that stores the merchandise items each game tour"""
    __tablename__='merchandise'
    id = Column(Integer(), primary_key=True, nullable=False)
    item_name = Column(String(100), nullable=False)
    item_price = Column(Numeric(10, 2), nullable=False)
    total_quantity = Column(Integer(), nullable= False)
    date_added = Column(DATE(), default=datetime.now)

    # sale = relationship('Sales',back_populates='merchandise_item')
    def __str_(self):
        merchandise_record ='Merchandise item id={} item_name={} item_description={} item_price={}, total_quantity={} date_added={}'
        return merchandise_record.format(self.id, self.item_name, self.item_price, self.total_quantity, self.date_added)

class Sales(Base):
    """A table that holds sales information for each each merchandise item and game location"""
    __tablename__='sale'
    id = Column(Integer, primary_key=True, nullable=False)
    venue_id = Column(Integer(), ForeignKey('game_schedule.venue_id'))
    item_id = Column(Integer(), ForeignKey('merchandise.id'))
    quantity_sold = Column(Integer(), nullable=False)

    game = relationship('Game', backref=backref('sale', order_by=id))
    merchandise = relationship('Merchandise', backref=backref('sale', order_by=id))

    def __str__(self):
        sales_record = "Sale Details: id={}  venue_id={} quantity_sold={} "
        return sales_record.format(self.id,self.venue_id, self.item_id, self.quantity_sold)




Base.metadata.create_all(engine)
