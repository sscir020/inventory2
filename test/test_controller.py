import unittest
from app.models import User,Material,Opr
from app import db,create_app


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with  self.app.app_context():
            u = User(user_name='a', user_pass='1234')
            u.prt()
            # db.create_all()
            db.session.add(u)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()
