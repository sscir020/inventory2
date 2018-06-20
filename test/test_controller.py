import unittest

from config import db,app
# from application import create_app
from applicaiton.models import User,Material,Opr

class test_user(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
