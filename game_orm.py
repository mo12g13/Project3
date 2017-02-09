from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tour_details import Game, Merchandise, Sales
import datetime
from sqlalchemy.sql import func


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
            print("Please avoid entering characters. Please enter a valid number")
            continue
        return user_input_enter

#A method that validates the user input to ensure that valid price was entered
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
    while True:
        try:
            stadium_name = get_valid_user_input("Please enter the name for this stadium: ")
            new_location = get_valid_user_input("Please enter the city where {} stadium is located: ".format(stadium_name))
            game_schedule_date= get_valid_date('Please enter the schedule date for {} game. We only accept within 2017: '.format(new_location))
            new_game = Game(stadium=stadium_name, game_location=new_location, game_date=str(game_schedule_date))
            new_session.add(new_game)
            new_session.commit()

            print("Venue id:{} Stadium: {} Game location: {} Game date: {} Date added {}".format(new_game.venue_id,
            new_game.stadium, new_game.game_location,new_game.game_date,new_game.date_updated))
            print("Successfully added to the database")
            new_session.close()
            break
        except Exception as e:
            print(e)
            new_session.rollback() # rollback the database since there and error in saving the data
            new_game.venue_id=None
            new_game.stadium=None
            new_game.game_location=None
            new_game.game_date=None
            new_game.date_updated=None
            new_session.close()
            continue

#A method that adds items to the merchandise table
def add_new_merchandise_item(new_merchandise_session):
    while True:
        try:
            new_item_name =get_valid_user_input("Please enter the name of this item: ")
            new_item_price = get_price('Please enter the price for {}: '.format(new_item_name))
            quantities=get_integer('Please enter the quantity amount for {}'.format(new_item_name))
            new_merchandise = Merchandise(item_name=new_item_name, item_price=new_item_price, total_quantity=quantities)
            new_merchandise_session.add(new_merchandise)
            new_merchandise_session.commit()
            print('Item id: {} Price: {} Quanty: {} Date added: {}'.format(new_merchandise.item_name,
             new_merchandise.item_price, new_merchandise.total_quantity, new_merchandise.date_added))
            print("Successfully added to database")
            new_merchandise_session.close()
            break
        except:
            print("Error saving data to the database")
            new_merchandise_session.rollback() #rollback to previous time. Set all fields to None since there was an error in saving the data
            new_merchandise_session.id=None
            new_merchandise_session.item_name=None
            new_merchandise.item_price=None
            new_merchandise_session.total_quantity=None
            new_merchandise.date_added=None
            new_merchandise_session.close()
            continue

#Display data from the game database
def display_game_database(session_query):
    try:
        for game in session_query.query(Game):
            print('Venue id: {} Stadium: {} Game locatin: {} Game date: {} Date entered: {}'.format(game.venue_id, game.stadium,
            game.game_location, game.game_date, game.date_updated.isoformat()))
    except Exception as e:
        print(e)
        print("Error connecting to the database. Connection wasn't successful")

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
            sale_info.item_id, sale_info.quantity_sold, sale_info.date_enter))
            print("Successfully added to the database")

            sale_session.close()
            break
        except  Exception as e:
            print(e)
            print("Error saving data to the databases. Please make sure you enter the right venue id and sales id ")
            sale_session.rollback() # Roll back to previous point in time. Set all fields to NO since there was an error in saving the user data
            sale_info.id=None
            sale_info.venue_id=None
            sale_info.item_id=None
            sale_info.date_enter=None
            sale_info.total_quanity_amount=None
            continue

#Displays all items in the Merchandise table
def display_merchandise_data(session_query):
    try:
        for item in session_query.query(Merchandise):
            print('Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(item.id, item.item_name,
             item.item_price, item.total_quantity, item.date_added.isoformat()))
        session_query.close()
    except Exception as e:
        print("Couldn't read data from database. Database connection error")
        print(e)

#A method that display the update menu for each table
def update_tables_info():
    print("Enter 1 to update items in the Merchandise table")
    print("Enter 2 to update information in the Game table")
    print("Enter 3 to update quantity amount in the Sales table ")
# A menu that dipslays the delete menu for each table
def delete_table_data():
    print("Enter 1 to delete a row in the Game table")
    print("Enter 2 to delete a row in the Merchandise table")
    print("Enter 3 to delte a row from Sales table ")


#Display the menu options for the user
def display_menus_options():
    print("Welcome to Team tour database")
    print("Menu options")
    print("Enter 1 to add new information to the Game table")
    print("Enter 2 to add new information to the Merchandise table")
    print("Enter 3 to add new information to Sales table")
    print("Enter 4 to update an information in either the Sales , Merchandise or Sales table")
    print("Enter 5 to delete a row from either the Sales Merchandise or Game table")
    print("Enter 6 search search which game had the highest salses")
    print("Enter 7 to exit the database")

#A method that is used to update the merchandise table
def update_merchandise_item():
    available_session = Session()
    while True:
        try:
            print("Items currently store in the merchandise table")
            display_merchandise_data(available_session)
            enter_choice = get_integer("Please enter item id you would want to update: ")
            update_item = available_session.query(Merchandise).filter_by(id=enter_choice).one()
            print('Item to be updated: Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(update_item.id, update_item.item_name,
            update_item.item_price, update_item.total_quantity, update_item.date_added.isoformat()))
            response = get_valid_user_input("Do you want to change {} Y/N? ".format(update_item.item_name)).lower()
            if response == "y":
                new_item = get_valid_user_input("Please enter item new name for {}: ".format(update_item.item_name))
                update_item.item_name = new_item
            elif response =='n':
                pass
            else:
                print("Entry not valid please enter a valid entry")
                continue
            response = get_valid_user_input("Do you want to change the price of {} Y/N? ".format(update_item.item_price)).lower()
            if response == 'y':
                new_price= get_price("Please enter new price for old price of {}: ".format(update_item.item_price))
                update_item.item_price = new_price
            elif response =='n':
                pass

            else:
                print("Entry not valid please enter a valid entry")
                continue
            response = get_valid_user_input("Do you want to change the current quantity of {} Y/N? ".format(update_item.total_quantity)).lower()
            if response == 'y':
                new_quantity = get_integer("Please enter new price for old price of {}: ".format(update_item.total_quantity))
                update_item.total_quantity = new_quantity
            elif response == 'n':
                pass
            else:
                print("Entry not valid please enter a valid entry")
                continue
            available_session.commit()
            print('Successfully updated to: Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(update_item.id, update_item.item_name,
            update_item.item_price, update_item.total_quantity, update_item.date_added.isoformat()))
            available_session.close()
            break
        except Exception as e:
            print("Error modifying data. Coudln't save data to the database")
            print(e)
            available_session.rollback()
            continue
# A method taht is called to update the game table
def update_game_table():
    available_session = Session()
    while True:
        try:
            print("Items currently store in the Game table")
            display_game_database(available_session)
            enter_choice = get_integer("Please enter venue id you would want to update: ")
            update_item = available_session.query(Game).filter_by(venue_id=enter_choice).one()
            print('Item to be updated: Venue id: {} Stadium name: {} Game location: {} Game date: {} Date added: {}'.format(update_item.venue_id, update_item.stadium,
            update_item.game_location, update_item.game_date, update_item.date_updated.isoformat()))
            response = get_valid_user_input("Do you want to change {} Y/N? ".format(update_item.stadium)).lower()
            if response == "y":
                new_stadium = get_valid_user_input("Please enter item new name for {}: ".format(update_item.stadium))
                update_item.stadium = new_stadium
            elif response =='n':
                pass

            else:
                print("Entry not valid please enter a valid entry")
                continue
            response = get_valid_user_input("Do you want to change the game location for {} Y/N? ".format(update_item.game_location)).lower()
            if response == 'y':
                new_location= get_valid_user_input("Please enter new game location  {} game: ".format(update_item.game_location))
                update_item.game_location = new_location
            elif response =='n':
                pass
            else:
                print("Entry not valid please enter a valid entry")
                continue
            response = get_valid_user_input("Do you want want to change the game date of  {}Y/N? ".format(update_item.game_date)).lower()
            if response == 'y':
                new_date = get_valid_date("Please enter new date to replace {} date Date format: YYYY/MM/DD or YYYY-MM-DD for 2017 only: ".format(update_item.game_date))
                update_item.game_date = new_date
            elif response == 'n':
                pass
            else:
                print("Entry not valid please enter a valid entry")
                continue
            date_updated = datetime.datetime.now()
            available_session.commit()
            print('Successfully updated to: Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(update_item.venue_id, update_item.stadium,
            update_item.game_location, update_item.game_date, update_item.date_updated.isoformat()))
            available_session.close()
            break
        except Exception as e:
            print("Error modifying data. Coudln't save data to the database")
            print(e)
            available_session.rollback()
            continue

# A method that is called to update the sales table
def update_sales_table():

        new_session_to_update = Session()
        while True:
            try:
                print("Items currently store in the Game table")

                enter_choice = get_integer("Please enter sale id you would want to update: ")
                update_item = new_session_to_update.query(Sales).filter_by(id=enter_choice).one()
                print('Item to be updated: Sale id: {} Venue id: {} Item id: {} Quantity sold: {} Date added: {}'.format(update_item.id, update_item.venue_id,
                update_item.item_id, update_item.quantity_sold, update_item.date_enter.isoformat()))
                response = get_valid_user_input("Do you want to change venue id {} Y/N? ".format(update_item.venue_id)).lower()
                if response == "y":
                    venue_new_id = get_valid_user_input("Please new venue id for venue id {}: ".format(update_item.venue_id))
                    update_item.venue_id = venue_new_id
                elif response =='n':
                    pass
                else:
                    print("Entry not valid please enter a valid entry")
                    continue
                response = get_valid_user_input("Do you want to change item id {} Y/N? ".format(update_item.item_id)).lower()
                if response == 'y':
                    new_id_item= get_valid_user_input("Please enter new item id for item id {}: ".format(update_item.item_id))
                    update_item.item_id = new_id_item
                elif response =='n':
                    pass
                else:
                    print("Entry not valid please enter a valid entry")
                    continue
                response = get_valid_user_input("Do you want to change the quanty of {}Y/N? ".format(update_item.quantity_sold)).lower()
                if response == 'y':
                    new_quantity= get_integer("Please enter new quantity amount for {}: ".format(update_item.quantity_sold))
                    update_item.quantity_sold = new_quantity
                elif response == 'n':
                    pass
                else:
                    print("Entry not valid please enter a valid entry")
                    continue
                date_enter= datetime.datetime.now()
                new_session_to_update.commit()
                print('Successfully updated to: Sale id: {} Venu id: {}  Item id: {} Quantity {} Date added: {}'.format(update_item.id, update_item.venue_id,
                update_item.item_id, update_item.quantity_sold, update_item.date_enter.isoformat()))
                new_session_to_update.close()
                break
            except Exception as e:
                print("Error modifying data. Coudln't save data to the database")
                print(e)
                new_session_to_updaten.rollback()
                continue
# A method that deletes row in the Game table
def delete_game_table_row():
    game_delete_session = Session()
    while True:
        try:
            user_input = get_integer("Please enter the game id of the row you want to delete: ")
            for delete_row in game_delete_session.query(Game).filter_by(venue_id=user_input):
                game_delete_session.delete(delete_row)
            print('Row successfully deleted: Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(delete_row.venue_id, delete_row.stadium,
            delete_row.game_location, delete_row.game_date, delete_row.date_updated.isoformat()))
            game_delete_session.commit()
            game_delete_session.close()
            break
        except Exception as e:
            print(e)
            print("Error deleting data from the database")
            delete_session.rollback()
            delete_session.close()
            continue
# A method that deletes row in the Merchandise table
def dele_merchandise_table_row():
    merchandise_delete_session = Session()
    while True:
        try:
            user_input = get_integer("Please enter the item id of the row you want to delete: ")
            for delete_row in merchandise_delete_session.query(Merchandise).filter_by(id=user_input):
                merchandise_delete_session.delete(delete_row)
            print('Row successfully deleted: Item id: {} Item name: {} Price: {} Quanty: {} Date added: {}'.format(delete_row.id, delete_row.item_name,
            delete_row.item_price, delete_row.total_quantity, delete_row.date_added.isoformat()))
            merchandise_delete_session.commit()
            merchandise_delete_session.close()
            break
        except Exception as e:
            print(e)
            print("Error deleting data from the database")
            merchandise_delete_session.rollback()
            merchandise_delete_session.close()
            continue
# A method that deletes a row in the sales table
def delete_sales_table_row():
    sales_delete_session = Session()
    while True:
        try:
            user_input = get_integer("Please enter the Sales id of the row you want to delete: ")
            for delete_row in sales_delete_session.query(Sales).filter_by(id=user_input):
                sales_delete_session.delete(delete_row)
            print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: {} Date entered: {}'.format(delete_row.id, delete_row.venue_id,
            delete_row.item_id, delete_row.quantity_sold, delete_row.date_enter.isoformat()))
            sales_delete_session.commit()
            sales_delete_session.close()
            break
        except Exception as e:
            print(e)
            print("Error deleting data from the database")
            sales_delete_session.rollback()
            sales_delete_session.close()
            continue

# Display data from the sales table
def display_sale_table(session_query):
    try:
        for sales in session_query.query(Sales):
            print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: {} Date entered: {}'.format(sales.id, sales.venue_id,
            sales.item_id, sales.quantity_sold, sales.date_enter.isoformat()))
        session_query.close()
    except Exception as e:
        print(e)
        print("Connection error" "database connection wasn't successful")
        session_query.close()
#A method that finds the max quantity venue_id, item_id that had the highest sales
def find_max_quantity_amount():
    try:
        print("Venue with the hight sales quantity")
        max_session = Session()
        query = max_session.query(Sales).order_by(Sales.quantity_sold.desc()).first()
        print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: {} Date entered: {}'.format(query.id, query.venue_id,
        query.item_id, query.quantity_sold, query.date_enter.isoformat()))
        max_session.close()
    except Exception as e:
        print("Error has occured. Couldn't restrieve the max quantity sold from the database")
        print(e)
        max_session.rollback()
        max_session.close()

def main():
    while True:
        display_menus_options()
        choice = get_integer("Please enter a choice from the menu: ")
        #if choice is 1, ask the user if they actually wants to add information to the game table. If user_choice is y display the game table and ask the user for inputs
        if choice == 1:
            user_choice = get_valid_user_input("Are you sure you want to enter data in the Game table? Please enter Y/N? ").lower()
            if user_choice =='y':
                print("information currently available in the game table")
                display_game_database(session)
                add_new_game_location_info(session)
            else:
                continue
        #if choice is 2, ask the user if they actually wants to add information to the merchandise table. If user_choice is y display the merchandise database and ask the user for inputs
        elif choice == 2:
            user_choice = get_valid_user_input("Are you sure you want to enter data in the Merchandis table? Please enter Y/N? ").lower()
            if user_choice == 'y':
                print("Items currently store in the in merchandise table: ")
                display_merchandise_data(session)
                add_new_merchandise_item(session)
            else:
                continue
            #if choice is 3, ask the user if they actually wants to add information to the Sales table. If user_choice is y display the game and merchandise table and ask the user for inputs
        elif choice == 3:
            user_choice = get_valid_user_input("Are you sure you want to enter data in the Sales table? Please enter Y/N? ").lower()
            if user_choice == 'y':
                print("Current game schedule store in the database")
                display_game_database(session)
                print('\n')
                print("Current merchandise store in the database")
                print('\n')
                display_merchandise_data(session)
                print("current sales information in our database")
                display_sale_table(session)
                add_sale_info(session)
            else:
                continue
        elif choice == 4: #Choice to update information within this database
            user_choice = get_valid_user_input("Are you sure you want to update information in the database Y/N? ").lower()
            if user_choice == 'y':
                update_tables_info()
                choice_made = get_integer("Please enter menu choice: ")
                if choice_made ==1:
                    print("Current information store in the merchandise table")
                    display_merchandise_data(session)
                    update_merchandise_item()
                elif choice_made== 2:
                    display_game_database(session)
                    update_game_table()
                elif choice_made == 3:
                    display_sale_table(session)
                    update_sales_table()
        elif choice == 5: # If choice is equals 5 as confirm if user what wants delete information from the database and display the appropriate menu
            valid_choice = get_valid_user_input("Are you sure you want to delete information in the database Y/N? ").lower()
            if valid_choice =='y':
                delete_table_data()
                user_choice = get_integer("Please enter menu choice")
                if user_choice == 1:
                    display_game_database(session)
                    delete_game_table_row()
                elif user_choice == 2:
                    display_merchandise_data(session)
                    dele_merchandise_table_row()
                elif user_choice == 3:
                    display_sale_table(session)
                    delete_sales_table_row()
        elif choice == 6:
            find_max_quantity_amount()
        elif choice == 7:
            print("Shutting the database....")
            session.close()
            session.commit()
            break

            break





if __name__=='__main__':
    main()
