from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tour_details import Game, Merchandise, Sales

engine = create_engine('sqlite:///game_tour.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

game_one = Game(stadium='Vikings Stadium', game_location="Minneapolis",game_date='2017-11-04')
game_tow = Game(stadium="Ohio Stadium", game_location="Columbus", game_date='17-15-05')

session.add(game_tow)
session.commit()
session.close()
for game in session.query(Game):
    print('Game Date: '+ game_one.game_date +' Game Location: '+ game.game_location+" Game updated date: "+ game.date_updated.strftime("%d/%m/%y"))

# merchand = Merchandise(item_decription='Hat', item_price=4.50)
# session.add(merchand)
# session.commit()
#
# print(merchand.id, merchand.item_decription, merchand.item_price)
#
# sale = Sales(quantity_sold=20)
# session.add(sale)
# session.commit()
# print(sale.id,sale.venue_id, sale.item_id, sale.quantity_sold)
