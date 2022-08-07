from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_start_screen(self):
        """tests that the homepage appears and displays image correctly"""
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.satus_code, 200)
            self.assertIn('<img src="https://pbs.twimg.com/media/FPRlsAqWQAYd8fj?format=jpg&name=360x360" alt="Peggy Hill">', html)

    def test_game_start(self):
        """tests that the game board gets put into the session"""
        with self.client:
            resp = self.client.get('/game')
            self.assertIn('board', session)

    def test_valid_answer(self):
        """tests a valid answer submittal"""
        with self.client as client:
            with client.session_transaction() as sesh:
                sesh['board'] =  [["Q","E","D","S","G"],
                ["F","Z","N","R","C"],
                ["J","E","G","F","K"],
                ["O","P","A","T","D"],
                ["E","S","I","M","S"]]
        response = self.client.get('/check?word=pat')
        self.assertEqual(response.json['result'], 'ok')

    def test_not_on_board(self):
        """tests an invalid answer submittal"""
        with self.client as client:
            with client.session_transaction() as sesh:
                sesh['board'] =  [["Q","E","D","S","G"],
                ["F","Z","N","R","C"],
                ["J","E","G","F","K"],
                ["O","P","A","T","D"],
                ["E","S","I","M","S"]]
        response = self.client.get('/check?word=crunch')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_word(self):
        """tests submittal of something that's not a word"""
        self.client.get('/')
        response = self.client.get('check?word=gsdfgjhghsjklhfahfuioehuiosdghsfghs')
        self.assertEqual(response.json['result'], 'not-word')

 