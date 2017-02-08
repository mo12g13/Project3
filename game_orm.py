from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tour_details import Game, Merchandise, Sales
import datetime

#Connection of sqlite database for this project
engine = create_engine('sqlite:///game_tour.db', echo=False)
Session = sessionmaker(bind=engine) #session for this database
session = Session()

# A method that checks to make sure the date is in a specific format. Only 2017 is consider for this method

def get_valid_date(display_message):
    date_enter=""

    while True:
        date_enter=input(display_message)
        try:


            if '/' in date_enter and len(date_enter)==10 and date_enter[0:4]=='2017' and len(date_enter[5:7])==2 and len(date_enter[8:])==2:
                new_date =date_enter =date_enter.split('/')
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

#A method that validates the user input to make user the user enters a valid input
def get_valid_user_input(display_message):
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
def get_integer(display_message):
    user_input_enter =''
    while  True:
        try:
            user_input_enter = int(input(display_message))
            if user_input_enter > 0:
                pass
            elif user_input_enter < 0 or user_input_enter == 0:
                print('Please  enter a value greater than zero')
                continue
        except ValueError:
            print("Please avoid entering characters. you were asked to enter quantity amount")
            continue
        return user_input_enter

#A method that validate the user input to ensure that valid price was entered
def get_price(message_display):
    input_price=''
    while True:
            try:
                input_price=float(input(message_display))
                if input_price <0.00 or input_price == 0.00:
                    print('Price must be number greater than zero')
                    continue
                elif input_price > 0:
                    break
                else:
                    print("an input error occur, please review your input")
                    continue
            except ValueError:
                print("Please enter decimal number! characters or invalid input can't be price")
                continue
    return input_price



# A method that adds a new game information to the database. For instance, if we have a new game information, the user can add that game information

def add_new_game_location_info(new_session):
    stadium_name = get_valid_user_input("Please enter the name for this stadium: ")
    new_location = get_valid_user_input("Please enter the city where {} stadium is located: ".format(stadium_name))
    game_schedule_date= get_valid_date('Please enter the schedule date for {} game. We only accept within 2017'.format(new_location))
    new_game = Game(stadium=stadium_name, game_location=new_location, game_date=str(game_schedule_date))
    new_session.add(new_game)
    new_session.commit()

    print("Venue id:{} Stadium: {} Game location: {} Game date: {} Date added {}".format(new_game.venue_id,
    new_game.stadium, new_game.game_location,new_game.game_date,new_game.date_updated))
    print("Successfully added to the database")
    new_session.close()

#A method that adds items to the merchandise table
def add_new_merchandise_item(new_merchandise_session):
    new_item_name =get_valid_user_input("Please enter the name of this item: ")
    new_item_price = get_price('Please enter the price for {}: '.format(new_item_name))
    quantities=get_integer('Please enter the quantity amount for {}'.format(new_item_name))
    new_merchandise = Merchandise(item_name=new_item_name, item_price=new_item_price, total_quantity=quantities)
    new_merchandise_session.add(new_merchandise)
    new_merchandise_session.commit()
    print('Item id: {} Price: {} Quanty: {} Date added: {}'.format(new_merchandise.item_name,
     new_merchandise.item_price, new_merchandise.total_quantity, new_merchandise.date_added))
    print("Successfully added to database")
    session.close()

#A method the use to add venue_id, item_id and quantity for merchandise and game table
def add_sale_info(sale_session):
    while True:
        try:

            new_venue_id = get_integer("Please enter the venue id for game table: ")
            new_item_id = get_integer("Please enter the item id from the merchandise talbe:  ")
            total_quanity_amount = get_integer("Please enter the quantity that was sold from the sales table: ")
            sale_info = Sales(venue_id=new_venue_id, item_id=new_item_id, quantity_sold=total_quanity_amount)
            sale_session.add(sale_info)
            sale_session.commit()
            print("Sales id: {} Venue id: {} Item id: {} Total Quanity: {}".format(sale_info.id, sale_info.venue_id,
            sale_info.item_id, sale_info.total_quanity_amount, sale_info.date_enter))
            print("Successfully added to the database")
            session.close()
            break
        except:
            print("Error saving data to the databases")
            sale_session.rollback() # Roll back to previous point in time since there was an error in saving the user data
            sale_info.id=None
            sale_info.venue_id=None
            sale_info.item_id=None
            sale_info.date_enter=None
            sale_info.total_quanity_amount=None
            continue







game_one = Game(stadium='Vikings Stadium', game_location="Minneapolis",game_date='2017-11-04')
game_two= Game(stadium="Ohio Stadium", game_location="Columbus", game_date='2017-15-05')
game_three= Game(stadium='Bryant–Denny Stadium', game_location='Tuscaloosa', game_date='2017-22-14')
game_four = Game(stadium='Cotton Bowl', game_location='Dallas', game_date='2017-12-13')


for game in session.query(Game):
    print(game)
add_sale_info(session)
# add_new_merchandise_item(session)
# add_new_game_location_info(session)
# merchand = Merchandise(item_decription='Hat', item_price=4.50)
