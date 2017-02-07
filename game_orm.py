from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tour_details import Game, Merchandise, Sales
import datetime

engine = create_engine('sqlite:///game_tour.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# A method that checks to make sure the date is in a specific format

def valid_date(display_message):
    date_enter=""

    while True:
        try:
            date_enter=input(display_message)
            if '/' in date_enter and len(date_enter)==10 and date_enter[0:4] is'2017' and len(date_enter[5:7])==2 and len(date_enter[8:])==2:
                new_date = date_enter.split('/')
                new_date = datetime.date(year=int(date_enter[0]), month=int(date_enter[1]), day=int(date_enter[2]))

                break
            elif '-' in date_enter and len(date_enter)==10 and date_enter[0:4]=='2017' and len(date_enter[5:7])==2 and len(date_enter[8:])==2:
                new_date=date_enter=date_enter.split('-')
                new_date = datetime.date(year=int(date_enter[0]), month=int(date_enter[1]), day=int(date_enter[2]))

                break
            else:
                print("Please a date in the following format YYYY-MM-DD/YYYY/MM/DD")
                continue
        except ValueError:
            print("Please enter a valid date. The year, month or day was higher than expected")
            continue
    new_date.timetuple()
    return new_date

valeud= valid_date("Please enter a date in the format YYYY-MM-DD/YYYY/MM/DD: ")

print(valeud)


#A method that validates the user input to make user the user enters a valid input
def validate_user_input(display_message):
    user_input =""
    while True:
        user_input=input(display_message)
        if user_input =='':
            print('Please enter a valid text, No empty is allowed')
            continue
        elif user_input[0].isdigit():
            print("Please enter a valid name. Name shouldn't start with number/numbers")
            continue
        else:
            break
    return user_input

# A method that checks and make the user enter a valid Integer
def valid_integer_enter(display_message):
    user_input_enter =''
    while  True:
        try:
            user_input_enter = int(input(display_message))
            if user_input_enter > 0:
                pass
            elif user_input_enter < 0:
                print('Please  enter a value greater than zero')
                continue
        except ValueError:
            print("Please avoid entering characters. you were as to enter quantity")
            continue
        return user_input_enter

number_enter = valid_integer_enter("Please enter quantity")
print(number_enter)

valid_input = validate_user_input("Please enter game date:")
print(valid_input)


game_one = Game(stadium='Vikings Stadium', game_location="Minneapolis",game_date='2017-11-04')
game_two= Game(stadium="Ohio Stadium", game_location="Columbus", game_date='2017-15-05')
game_three= Game(stadium='Bryant–Denny Stadium', game_location='Tuscaloosa', game_date='2017-22-14')
game_four = Game(stadium='Cotton Bowl', game_location='Dallas', game_date='2017-12-13')



# session.add_all([game_one, game_two, game_three, game_four])

session.commit()
session.close()
for game in session.query(Game):
    print('venue id: '+ str(game.venue_id) + ' Game Date: '+ str(game.game_date) +' Game Location: '+ str(game.game_location) +" Date added: "+ str(game.date_updated.strftime("%d/%m/%y")))

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
