import unittest
import api

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.email = open('tests/.email').read().strip()
        self.password = open('tests/.pw').read().strip()

    def test_login_and_logout(self):
        s = api.login(self.email, 'lololololol')
        assert not s.is_authenticated

        s = api.login(self.email, self.password)
        assert s.is_authenticated

        s.logout()
        assert not s.is_authenticated

    def test_register_for_class_and_unregister(self):
        with api.login(self.email, self.password) as s:
            s.register_for_class(379333)
            s.unregister_for_class()





