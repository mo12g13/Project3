import unittest
import game_orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tour_details


# There is bug that I couldn't figure out. when you keep running the test, it keeps adding merchandise rows and as
#well as delete data from the database. I will figure out this bug.
class TestGameOrm(unittest.TestCase):
    test_db = 'sqlite:///game_tour.db'

    def setUp(self):
        game_orm.engine = create_engine(self.test_db, echo=False)
        game_orm.Session = sessionmaker(bind=game_orm.engine)
        game_orm.session = game_orm.Session()
        self.session = game_orm.session
        tour_details.Base.metadata.create_all(game_orm.engine)

    # def tearDown(self):
    #     tour_details.Base.metadata.drop_all(game_orm.engine)
    #     game_orm.session.close()

    # Testing of the price method
    def test_get_price(self):
        number_enter = 6
        self.assertEqual(number_enter, game_orm.enter_input(6))


    # Testing of the valid date method
    def test_valid_date(self):
        date_enter = '2017-12-14'
        self.assertEqual(date_enter, game_orm.valid_date('2017-12-14'))

    def test_date_not_valid(self):
        date ='2017-32-12'
        self.assertNotEqual(date, game_orm.valid_date('2017-12-12'))


    # Testing of valid integer method
    
    def test_valid_integer(self):
        number = 5
        self.assertEqual(number, game_orm.valid_integer(5))


    # Testing of the user_enter_price method
    def test_user_enter_price(self):
        price = 50.00
        self.assertEqual(price, game_orm.user_enter_price(50.00))

    # Testing of the add game info method that adds a game to the database
    def test_add_new_game_info_table(self):
        game_stadium= 'Target'
        location = "Minneapolis"
        date = '2017-12-12'
        game_orm.add_game_info(game_stadium, location, date)
        game = self.session.query(tour_details.Game).filter_by(stadium=game_stadium, game_location=location, game_date=date).one_or_none()
        self.assertIsNotNone(game)

    def test_add_new_merchandise_item(self):
        name_of_item = 'Hat'
        price_of_item = 14.99
        quantity_amount = 304

        # function to test
        game_orm.add_new_merchandise_item(name_of_item, price_of_item, quantity_amount)

       # Also test that date_added is correct
        hat = self.session.query(tour_details.Merchandise).filter_by(item_name=name_of_item, item_price=price_of_item, total_quantity=quantity_amount).one_or_none()
        self.assertIsNotNone(hat)

    # Testing of the merchandise table
    def test_update_merchandise_table(self):
        name_of_item = "Jersey"
        price_of_item = 12.00
        quantity = 503
        update_item = self.session.query(tour_details.Merchandise).filter_by(item_name='Hat', item_price=14.99, total_quantity=304).one_or_none()
        game_orm.update_merchandise_item(name_of_item, price_of_item, quantity, update_item)
        self.assertIsNotNone(update_item)

    # Testing the update game method
    def test_update_game_table(self):
        new_stadium = 'Vikings'
        new_location = 'Minneapolis'
        new_game_date = '2017-12-04'

        update_game = self.session.query(tour_details.Game).filter_by(stadium='Target', game_location='Minneapolis', game_date ='2017-12-12').one_or_none()
        game_orm.update_game_table(new_stadium, new_location, new_game_date, update_game)
        self.assertIsNotNone(update_game)

    # Testing the delete method of delete sales table row

    def test_delete_game_table_row(self):
        for delete_row in self.session.query(tour_details.Game).filter_by(stadium='Target', game_location='Minneapolis', game_date='2017-12-12').one_or_none():

            self.assertIsNotNone(delete_row)
    # Testing of the delete sales table method

    def test_delete_merchandise_table_row(self):
        for delete_row in self.session.query(tour_details.Merchandise).filter_by(item_name='Hat', item_price=14.99, total_quantity=304).one_or_none():
            self.assertIsNotNone(delete_row)







if __name__=='__main__':
    unittest.main()
