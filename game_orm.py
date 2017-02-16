from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tour_details import Game, Merchandise, Sales
import datetime

# Connection of SQLite database for this project
engine = create_engine('sqlite:///game_tour.db', echo=False)
Session = sessionmaker(bind=engine) # session for this database
session = Session()
# A method that checks to make sure the date is in a specific format. Only 2017 is consider for this method


def valid_date(date_enter_by_user):
    while True:

        try:
            if '/' in date_enter_by_user and len(date_enter_by_user) == 10 and date_enter_by_user[0:4] == '2017' and len(date_enter_by_user[5:7]) == 2 and len(date_enter_by_user[8:]) == 2:
                new_date = date_enter_by_user = date_enter_by_user.split('/')
                new_date = datetime.date(year=int(date_enter_by_user[0]), month=int(date_enter_by_user[1]), day=int(date_enter_by_user[2]))
                break
            elif '-' in date_enter_by_user and len(date_enter_by_user) == 10 and date_enter_by_user[0:4] == '2017' and len(date_enter_by_user[5:7]) == 2 and len(date_enter_by_user[8:]) == 2:
                new_date=date_enter_by_user = date_enter_by_user.split('-')
                new_date = datetime.date(year=int(date_enter_by_user[0]), month=int(date_enter_by_user[1]), day=int(date_enter_by_user[2]))

                break
            else:
                print("Please enter date in the following format YYYY-MM-DD/YYYY/MM/DD. Year should only be in 2017")
                continue
        except ValueError:
            print("Please enter a valid date. The year, month or day was higher than expected")
            continue

    new_date.timetuple()

    return new_date.isoformat()

# A method that validates the user input to make user the user enters a valid input


def valid_user_input(display_message):
    user_enter_input = ""
    while True:
        user_enter_input = input(display_message)
        if user_enter_input == ' ':
            print('Please enter a valid text, No empty is allowed')
            continue
        else:
            break
    return user_enter_input


def enter_input(user_input_enter):
    while True:
        try:

            if user_input_enter > 0:
                pass
            elif user_input_enter < 0 or user_input_enter == 0:
                print('Please  enter a value greater than zero')
                continue
        except ValueError:
            print("Please avoid entering characters. Please enter a valid number")
            continue
        return user_input_enter

# A method that checks and make the user enter a valid Integer


def valid_integer(user_input_enter):

    enter_value = 0
    try:
        enter_value = int(user_input_enter)
        if enter_value > 0:
            pass

        elif enter_value < 0 or enter_value == 0:
            print('Please  enter a value greater than zero')

    except ValueError:
        print("Please avoid entering characters. Please enter a valid number")

    return enter_value


# A method that validates the user input to ensure that valid price was entered


def user_enter_price(price_enter):
    while True:
        input_price = 0

        try:
            input_price = float(price_enter)
            if input_price < 0.00 or input_price == 0.00:
                print('Price must be number greater than zero')
                continue

            elif input_price > 0:
                pass
            else:
                print("an input error occur, please review your input")
                continue

        except ValueError:
            print("Please enter decimal number! characters or invalid input can't be price")
            continue

        return input_price


# A method that adds a new game information to the database.
# For instance, if we have a new game information, the user can add that game information

def add_game_info(stadium_name, new_location, game_schedule_date):

    try:
        new_game = Game(stadium=stadium_name, game_location=new_location, game_date=game_schedule_date)
        session.add(new_game)
        session.commit()
        print('Venue id:{} Stadium: {} Game location: {} Game date: {} Date added {}'.format(new_game.venue_id, new_game.stadium, new_game.game_location,new_game.game_date,new_game.date_updated))
        print("Successfully added to the database")
        session.close()

    except Exception as e:
        print(e)
        session.rollback() # rollback the database since there and error in saving the data

        session.close()


# A method that adds items to the merchandise table


def add_new_merchandise_item(new_item_name, new_item_price, quantities):
    try:
        new_merchandise = Merchandise(item_name=new_item_name, item_price=new_item_price, total_quantity=quantities)
        session.add(new_merchandise)
        session.commit()
        print('Item id: {} Item name: {} Price: {} Quantity: '\
         '{} Date added: {}'.format(new_merchandise.id, new_merchandise.item_name, new_merchandise.item_price, new_merchandise.total_quantity, new_merchandise.date_added))
        print("Successfully added to database")
        session.close()
    except Exception as e:
        print(e)
        print("Error saving data to the database")
        session.rollback() # Rollback to previous time. Set all fields to None since there was an error in saving the data
        session.close()


# Display data from the game database


def display_game_database():
    try:
        for game in session.query(Game):
            print('Venue id: {} Stadium: {} Game location: {} Game date: {} Date'\
             ' entered: {}'.format(game.venue_id, game.stadium, game.game_location,
                                   game.game_date, game.date_updated.strftime("%A %d. %B %Y")))
            session.close()
    except Exception as e:
        print(e)
        print("Error connecting to the database. Connection wasn't successful")


# A method the use to add venue_id, item_id and quantity for merchandise and game table
def add_sale_info(new_venue_id, new_item_id, total_quantity_amount):

    try:
        sale_info = Sales(venue_id=new_venue_id, item_id=new_item_id, quantity_sold=total_quantity_amount)
        session.add(sale_info)
        session.commit()
        print('Sales id: {} Venue id: {} Item id:'\
         '{} Total Quantity: {}'.format(sale_info.id, sale_info.venue_id,
                                       sale_info.item_id, sale_info.quantity_sold, sale_info.date_enter))
        print("Successfully added to the database")
        session.close()

    except Exception as e:
        print(e)
        print("Error saving data to the databases. Please make sure you enter the right venue id and sales id ")
        session.rollback() # Rollback the database
        session.close()


# Displays all items in the Merchandise table


def display_merchandise_data():
    try:
        for item in session.query(Merchandise):
            print('Item id: {} Item name: {} Price: {} Quantity:'\
             '{} Date added: {}'.format(item.id, item.item_name,
                                       item.item_price, item.total_quantity, item.date_added.isoformat()))
        session.close()
    except Exception as e:
        print("Couldn't read data from database. Database connection error")
        print(e)

# A method that display the update menu for each table


def update_table_option():
    print("Enter 1 to update items in the Merchandise table")
    print("Enter 2 to update information in the Game table")
    print("Enter 3 to update quantity amount in the Sales table ")
# A menu that displays the delete menu for each table


def delete_table_option():
    print("Enter 1 to delete a row in the Game table")
    print("Enter 2 to delete a row in the Merchandise table")
    print("Enter 3 to delete a row from Sales table ")

# Display the menu options for the user


def display_menus_options():
    print("Welcome to Team tour database")
    print("Menu options")
    print("Enter 1 to add new information to the Game table")
    print("Enter 2 to add new information to the Merchandise table")
    print("Enter 3 to add new information to Sales table")
    print("Enter 4 to update an information in either the Sales , Merchandise or Sales table")
    print("Enter 5 to delete a row from either the Sales Merchandise or Game table")
    print("Enter 6 search search which game had the highest sales")
    print("Enter 7 to display merchandise table")
    print('Enter 8 to display sales table')
    print('Enter 9 to display game table')
    print("Enter 10 to exit the database")

# A method that is used to update the merchandise table


def update_merchandise_item(new_item,  new_price, new_quantity, update_item):

    try:
        update_item.item_name = new_item
        update_item.item_price = new_price
        update_item.total_quantity = new_quantity
        session.commit()
        print('Successfully updated to: Item id: {} Item name: {} Price: {} Quantity:'\
         ' {} Date added: {}'.format(update_item.id, update_item.item_name,
                                   update_item.item_price, update_item.total_quantity,
                                   update_item.date_added.isoformat()))
        session.close()

    except Exception as e:
        print("Error modifying data. Couldn't save data to the database")
        print(e)
        session.rollback()

# A method that is called to update the game table


def update_game_table(new_stadium, new_location, new_date, update_item):

   try:
        update_item.stadium = new_stadium
        update_item.game_location = new_location
        update_item.game_date = new_date

        session.commit()
        print('Successfully updated to: Item id: {} Item name: {}'\
         'Price: {} Quantity: {} Date'\
          'added: {}'.format(update_item.venue_id, update_item.stadium,
                            update_item.game_location, update_item.game_date, update_item.date_updated.isoformat()))
        session.close()

   except Exception as e:
        print("Error modifying data. Couldn't save data to the database")
        print(e)
        session.rollback()


# A method that is called to update the sales table


def update_sales_table(venue_new_id, new_id_item, new_quantity, update_item):

        update_item.venue_id = venue_new_id
        update_item.item_id = new_id_item
        update_item.quantity_sold = new_quantity
        try:
            session.commit()
            print('Successfully updated to: Sale id: {} Venue id: {}  Item id: {} Quantity '\
             '{} Date added: {}'.format(update_item.id, update_item.venue_id,
                                       update_item.item_id, update_item.quantity_sold,
                                       update_item.date_enter.isoformat()))
            session.close()
        except Exception as e:
            print("Error modifying data. Couldn't save data to the database")
            print(e)
            session.rollback()

# A method that deletes row in the Game table


def delete_game_table_row(user_response):

    try:

        for delete_row in session.query(Game).filter_by(venue_id=user_response):
            session.delete(delete_row)
        print('Row successfully deleted: venue id: {} Stadium: {} Game '\
              ' Location: {} Date added: {}'.format(delete_row.venue_id,
                                                   delete_row.stadium, delete_row.game_location,
                                                   delete_row.game_date, delete_row.date_updated.strftime("%A %d. %B %Y")))
        session.commit()
        session.close()

    except Exception as e:
        print(e)
        print("Error deleting data from the database")


# A method that deletes row in the Merchandise table

def delete_merchandise_table_row(response_of_user):

    try:
        for delete_row in session.query(Merchandise).filter_by(id=response_of_user):
            session.delete(delete_row)
        print('Row successfully deleted: Item id: {} Item name: {} Price: {} '\
        'Quantity: {} Date added: {}'.format(delete_row.id, delete_row.item_name,
                                            delete_row.item_price,
                                            delete_row.total_quantity, delete_row.date_added.isoformat()))
        session.commit()
        session.close()

    except Exception as e:
        print(e)
        print("Error deleting data from the database")
        session.rollback()
        session.close()

# A method that deletes a row in the sales table


def delete_sales_table_row(query_response):

    try:
        for delete_row in session.query(Sales).filter_by(id=query_response):
            session.delete(delete_row)
        print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: {} Date entered: '\
         '{}'.format(delete_row.id, delete_row.venue_id,
                    delete_row.item_id, delete_row.quantity_sold, delete_row.date_enter.isoformat()))
        session.commit()
        session.close()

    except Exception as e:
        print(e)
        print("Error deleting data from the database")
        session.rollback()
        session.close()


# Display data from the sales table


def display_sale_table():
    try:
        for sales in session.query(Sales):
            print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: '\
             '{} Date entered: {}'.format(sales.id, sales.venue_id,
                                         sales.item_id, sales.quantity_sold, sales.date_enter.isoformat()))
        session.close()
    except Exception as e:
        print(e)
        print("Connection error" "database connection wasn't successful")
        session.close()
# A method that finds the max quantity venue_id, item_id that had the highest sales


def find_max_quantity_amount():
    try:
        print("Venue with the highest sales quantity")
        max_session = Session()
        query_item = max_session.query(Sales).order_by(Sales.quantity_sold.desc()).first()
        print('Sales id: {}  Venue id: {} Iem id: {} Quantity sold: {}\
         Date entered: {}'.format(query_item.id, query_item.venue_id, query_item.item_id, query_item.quantity_sold,
                                  query_item.date_enter.isoformat()))
        max_session.close()
    except Exception as e:
        print("Error has occurred. Couldn't retrieve the max quantity sold from the database")
        print(e)
        max_session.rollback()
        max_session.close()

def main():
    while True:
        display_menus_options()

        choice = valid_integer(user_input_enter = input("Please enter a choice from the menu "))
        # if choice is 1, ask the user if they actually wants to add information to the game table.
        # If user_choice is y display the game table and ask the user for inputs
        if choice == 1:
            user_choice = valid_user_input("Are you sure you want to enter data in the Game table? Please enter Y/N? ").lower()
            if user_choice == 'y':
                print("Information currently available in the game table")
                display_game_database()
                stadium_name = valid_user_input("Please enter the name for this stadium: ")
                new_location = valid_user_input(
                    "Please enter the city where {} stadium is located: ".format(stadium_name))
                game_schedule_date = valid_date(date_enter_by_user = input('Please enter the schedule date for {} game. Valid year should be 2017:'.format(new_location)))

                add_game_info(stadium_name, new_location, game_schedule_date)
            else:
                continue

        # if choice is 2, ask the user if they actually wants to add information to the merchandise table.
        #  If user_choice is y display the merchandise database and ask the user for inputs
        elif choice == 2:
            user_choice = valid_user_input('Are you sure you want to enter data in the Merchandise table?'\
             'Please enter Y/N? ').lower()
            if user_choice == 'y':
                print("Items currently store in the in merchandise table: ")
                display_merchandise_data()
                new_item_name = valid_user_input("Please enter the name of this item: ")
                new_item_price = user_enter_price(price_enter= input('Please enter the price for {}: '.format(new_item_name)))
                quantities = valid_integer(user_input_enter = input('Please enter the quantity amount for {}'.format(new_item_name)))
                add_new_merchandise_item(new_item_name, new_item_price, quantities)
            else:
                continue
            #  if choice is 3, ask the user if they actually wants to add information to the Sales table.
            #  If user_choice is y display the game and merchandise table and ask the user for inputs
        elif choice == 3:
            user_choice = valid_user_input("Are you sure you want to enter data in the Sales table? Please enter Y/N? ").lower()
            if user_choice == 'y':
                print("Current game schedule store in the database")
                display_game_database()
                print('\n')
                print("Current merchandise store in the database")
                print('\n')
                display_merchandise_data()
                print("current sales information in our database")
                display_sale_table()
                new_venue_id = valid_integer(user_input_enter = input("Please enter the venue id for game table: "))
                new_item_id = valid_integer(user_input_enter= input("Please enter the item id from the merchandise table:  "))
                total_quantity_amount = valid_integer(user_input_enter = input("Please enter the quantity that was sold from the sales table: "))
                add_sale_info(new_venue_id,  new_item_id, total_quantity_amount)
            else:
                continue
        elif choice == 4: # Choice to update information within this database
            user_choice = valid_user_input("Are you sure you want to update information in the database Y/N? ").lower()
            if user_choice == 'y':
                update_table_option()
                choice_made = valid_integer(user_input_enter = input("Please enter menu choice: "))

                if choice_made == 1:
                    print("Current information store in the merchandise table")
                    display_merchandise_data()
                    enter_choice = valid_integer(user_input_enter = input("Please enter item id you would want to update: "))
                    if enter_choice > 0:
                        update_item = session.query(Merchandise).filter_by(id=enter_choice).one()
                        response = valid_user_input("Do you want to change {} Y/N? ".format(update_item.item_name)).lower()
                        if response == "y":
                            new_item = valid_user_input("Please enter item new name for {}: ".format(update_item.item_name))
                        elif response == 'n':
                            new_item = update_item.item_name
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue

                        response = valid_user_input("Do you want to change the price of {} Y/N? ".format(update_item.item_price)).lower()
                        if response == 'y':
                            new_price = user_enter_price(price_enter= input('Please enter new price for'\
                             ' old price of {}: '.format(update_item.item_price)))
                        elif response == 'n':
                            new_price = update_item.item_price

                        else:
                            print("Entry not valid please enter a valid entry")

                        response = valid_user_input('Do you want to change the current quantity of {}'\
                         'Y/N? '.format(update_item.total_quantity)).lower()
                        if response == 'y':
                            new_quantity = valid_integer(user_input_enter=input('Please enter new price for old price'\
                             ' of {}: '.format(update_item.total_quantity)))
                        elif response == 'n':
                            new_quantity = update_item.total_quantity
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue

                        update_merchandise_item(new_item,  new_price, new_quantity, update_item)
                    else:
                        print("Please enter a valid input")

                elif choice_made == 2:
                    print("Items currently store in the Game table")
                    display_game_database()
                    enter_choice = valid_integer(user_input_enter= input("Please enter venue id you would want to update: "))
                    if enter_choice >0:
                        update_item = session.query(Game).filter_by(venue_id=enter_choice).one()
                        print('Item to be updated: Venue id: {} Stadium name: {} Game location: {} Game date: {}' \
                              'Date added: {}'.format(update_item.venue_id, update_item.stadium,
                                                      update_item.game_location, update_item.game_date,
                                                      update_item.date_updated.isoformat()))
                        response = valid_user_input("Do you want to change {} Y/N? ".format(update_item.stadium)).lower()
                        if response == "y":
                            new_stadium = valid_user_input("Please enter item new name for {}: ".format(update_item.stadium))

                        elif response == 'n':
                            new_stadium = update_item.stadium

                        else:
                            print("Entry not valid please enter a valid entry")
                            continue
                        response = valid_user_input('Do you want to change the game location' \
                                              'for {} Y/N? '.format(update_item.game_location)).lower()
                        if response == 'y':
                            new_location = valid_user_input(
                                "Please enter new game location  {} game: ".format(update_item.game_location))
                        elif response == 'n':
                            new_location = update_item.game_location
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue
                        response = valid_user_input('Do you want want to change the game date'\
                                'of  {}Y/N? '.format(update_item.game_date)).lower()
                        if response == 'y':
                            new_date = valid_date(date_enter_by_user = input('Please enter the schedule date for {} game. Valid year should be 2017:'.format(new_location)))
                        elif response == 'n':
                            new_date = update_item.game_date

                        else:
                            print("Entry not valid please enter a valid entry")
                            continue

                        # display_game_database()
                        update_game_table(new_stadium, new_location, new_date, update_item)


                elif choice_made == 3:

                    print("Items currently store in the Game table")
                    display_sale_table()
                    enter_choice = valid_integer(user_input_enter = input("Please enter sale id you would want to update: "))
                    if enter_choice >0:
                        update_item = session.query(Sales).filter_by(id=enter_choice).one()
                        print('Item to be updated: Sale id: {} Venue id: {} Item id: {} Quantity sold: {}' \
                              'Date added: {}'.format(update_item.id, update_item.venue_id,
                                                      update_item.item_id, update_item.quantity_sold,
                                                      update_item.date_enter.isoformat()))
                        response = valid_user_input(
                            "Do you want to change venue id {} Y/N? ".format(update_item.venue_id)).lower()
                        if response == "y":
                            venue_new_id = valid_user_input("Please new venue id for venue id {}: ".format(update_item.venue_id))

                        elif response == 'n':
                            venue_new_id = update_item.venue_id
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue
                        response = valid_user_input("Do you want to change item id {} Y/N? ".format(update_item.item_id)).lower()
                        if response == 'y':
                            new_id_item = valid_user_input(
                                "Please enter new item id for item id {}: ".format(update_item.item_id))

                        elif response == 'n':
                            new_id_item = update_item.item_id
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue

                        response = valid_user_input(
                            "Do you want to change the quantity of {}Y/N? ".format(update_item.quantity_sold)).lower()
                        if response == 'y':
                            new_quantity = valid_integer(user_input_enter= input("Please enter new quantity amount\
                                   for {}: ".format(update_item.quantity_sold)))

                        elif response == 'n':
                            new_quantity = update_item.quantity_sold
                        else:
                            print("Entry not valid please enter a valid entry")
                            continue

                        update_sales_table(venue_new_id,new_id_item, new_quantity, update_item)
        elif choice == 5:  # If choice is equals 5 as confirm if the user what wants delete information from the database.
            # Display the appropriate menu
            valid_choice = valid_user_input("Are you sure you want to delete information in the database Y/N? ").lower()
            if valid_choice == 'y':
                delete_table_option()
                user_choice = valid_integer(user_input_enter = input("Please enter menu choice"))
                if user_choice == 1:

                    display_game_database()
                    user_response = valid_integer(user_input_enter= input("Please enter the game id of the row you want to delete: "))
                    delete_game_table_row(user_response)
                elif user_choice == 2:
                    display_merchandise_data()
                    response_of_user = valid_integer(user_input_enter=input("Please enter the item id of the row you want to delete: "))
                    delete_merchandise_table_row(response_of_user)
                elif user_choice == 3:
                    display_sale_table()
                    query_response = valid_integer(user_input_enter=input("Please enter the Sales id of the row you want to delete: "))
                    delete_sales_table_row(query_response)
        elif choice == 6:
            find_max_quantity_amount()
        elif choice == 7:
            display_merchandise_data()
        elif choice == 8:
            display_sale_table()
        elif choice == 9:
            display_game_database()
        elif choice ==10:
            print("Shutting down the database....")
            session.close()
            session.commit()

            break


if __name__ == '__main__':
    main()
