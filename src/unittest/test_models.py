import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .base import BaseTest
from .. import models


class Test(BaseTest):

    route = None

    def tearDown(self):
        if self.route:
            models.db.session.delete(self.route)
        models.db.session.commit()

    def test_db(self):
        self.assertIsInstance(models.db, SQLAlchemy)

    def test_RouteModel(self):
        self.route = models.RouteModel(path=str(uuid.uuid4()))
        models.db.session.add(self.route)
        models.db.session.commit()

        self.assertIsInstance(self.route, models.RouteModel)
        self.assertIsInstance(self.route.id, int)
        self.assertIsInstance(self.route.path, str)
        self.assertIsInstance(self.route.creation_date, datetime)
        self.assertIsInstance(self.route.expiration_date, datetime)

    def test_RouteModel_repr(self):
        self.route = models.RouteModel(path=str(uuid.uuid4()))
        models.db.session.add(self.route)
        models.db.session.commit()

        assert '<Route' in self.route.__repr__()
