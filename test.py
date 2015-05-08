import unittest
import main

class Test(unittest.TestCase):
    def test_get_csrf_token(self):
        main.get_csrf_token('lol')

    def test_get_seat(self):
        main.get_seat('lol')
