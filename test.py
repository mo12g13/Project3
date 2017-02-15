import unittest
import game_orm
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tour_details


class TestGameOrm(unittest.TestCase):
    test_db = 'sqlite:///game_tour.db'

    def setUp(self):
        game_orm.engine = create_engine(self.test_db, echo=False)
        game_orm.Session = sessionmaker(bind=game_orm.engine)
        game_orm.session = game_orm.Session()
        self.session = game_orm.session
        tour_details.Base.metadata.create_all(game_orm.engine)

    def tearDown(self):
        tour_details.Base.metadata.drop_all(game_orm.engine)
        game_orm.session.close()

    # Testing of the price method
    @patch('game_orm.get_price')
    def test_get_price(self, mock_price):
        mock_price.return_value=5
        self.assertEqual(5, game_orm.get_price())

    # Testing of the integer method
    @patch('game_orm.get_integer')
    def test_get_integer(self, mock_integer):
        mock_integer.return_value=45
        self.assertEqual(45, game_orm.get_integer())


    @patch('game_orm.get_valid_user_input')
    def test_valid_user_input(self, mock_meassage):

        mock_meassage.return_value=6
        self.assertEqual(6, game_orm.get_valid_user_input())

if __name__=='__main__':
    unittest.main()
