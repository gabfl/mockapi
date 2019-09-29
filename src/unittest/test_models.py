import uuid
from datetime import datetime

from dateparser import parse
from flask_sqlalchemy import SQLAlchemy

from .base import BaseTest
from .. import models


class Test(BaseTest):

    route = None
    route2 = None

    def tearDown(self):
        if self.route:
            models.db.session.delete(self.route)
        if self.route2:
            models.db.session.delete(self.route2)
        models.db.session.commit()

    def test_db(self):
        assert isinstance(models.db, SQLAlchemy)

    def test_db_auto_create(self):
        # The db should exist and the method is expected to return False
        assert models.db_auto_create() is False

    def test_db_auto_create_2(self):
        # Drop test table to force a db re-creation
        models.RouteModel.__table__.drop(models.db.engine)

        # The db will be created and the method is expected to return True
        assert models.db_auto_create() is True

    def test_RouteModel(self):
        self.route = models.RouteModel(path=str(uuid.uuid4()))
        models.db.session.add(self.route)
        models.db.session.commit()

        assert isinstance(self.route, models.RouteModel)
        assert isinstance(self.route.id, int)
        assert isinstance(self.route.path, str)
        assert isinstance(self.route.creation_date, datetime)
        assert self.route.expiration_date is None

        # Test with an expiration date
        self.route2 = models.RouteModel(
            path=str(uuid.uuid4()), expiration_date=parse('in 1 week'))
        models.db.session.add(self.route2)
        models.db.session.commit()

        assert isinstance(self.route2.expiration_date, datetime)

    def test_RouteModel_repr(self):
        self.route = models.RouteModel(path=str(uuid.uuid4()))
        models.db.session.add(self.route)
        models.db.session.commit()

        assert '<Route' in self.route.__repr__()
