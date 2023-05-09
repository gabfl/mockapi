import uuid
from dateparser import parse

from .base import BaseTest
from .. import routes_handler
from ..models import db, RouteModel
from ..bootstrap import get_or_create_app


class Test(BaseTest):

    route_1 = None
    route_2 = None

    def setUp(self):
        self.app = get_or_create_app()

    def tearDown(self):
        with self.app.app_context():
            if self.route_1:
                db.session.delete(self.route_1)
            if self.route_2:
                db.session.delete(self.route_2)
            db.session.commit()

    def test_new(self):
        with self.app.app_context():
            route = routes_handler.new()

            self.assertIsInstance(route, RouteModel)
            self.assertIsInstance(route.id, int)
            self.assertIsInstance(route.path, str)
            assert len(route.path) == 36

    def test_cleanup_old_routes(self):
        # Create 2 routes, one expired
        with self.app.app_context():
            self.route_1 = RouteModel(path=str(uuid.uuid4()), )
            db.session.add(self.route_1)
            self.route_2 = RouteModel(path=str(uuid.uuid4()),
                                      expiration_date=parse('1 month ago'))
            db.session.add(self.route_2)

            db.session.commit()

            # Call cleanup method
            routes_handler.cleanup_old_routes()

            # First route should exist
            self.assertIsInstance(RouteModel.query.filter_by(
                path=self.route_1.path).first(), RouteModel)

            # Second route should be deleted
            assert RouteModel.query.filter_by(
                path=self.route_2.path).first() is None
