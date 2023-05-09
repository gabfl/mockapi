import json

from .base import BaseTest
from .. import api_handler, routes_handler
from ..models import RouteModel
from ..bootstrap import get_or_create_app


class Test(BaseTest):

    def setUp(self):
        self.app = get_or_create_app()

    def test_hp(self):
        rv = self.client.get('/')
        assert rv.status_code == 200
        assert 'text/html' in rv.headers['Content-Type']

    def test_robots_txt(self):
        rv = self.client.get('/robots.txt')
        assert rv.status_code == 200
        assert b'User-Agent' in rv.data
        assert 'text/plain' in rv.headers['Content-Type']

    def test_favicon_ico(self):
        rv = self.client.get('/favicon.ico')
        assert rv.status_code == 200
        assert 'image/x-icon' in rv.headers['Content-Type']

    def test_new(self):
        rv = self.client.post('/new')
        assert rv.status_code == 200
        assert 'text/html' in rv.headers['Content-Type']

    def test_new_expires(self):
        rv = self.client.post('/new', data={'expire': 'in 1 week'})
        assert rv.status_code == 200
        assert 'text/html' in rv.headers['Content-Type']

    def test_api_invalid(self):
        rv = self.client.get('/api/some-invalid-path')
        assert rv.status_code == 307  # Will redirect to /404
        assert 'text/html' in rv.headers['Content-Type']

    def test_api_serve_json(self):
        body = '{"success": true}'

        # Generate a new route
        with self.app.app_context():
            route = routes_handler.new(
                type_='json',
                body=body
            )
            path = route.path

        rv = self.client.get('/api/' + path)
        assert rv.status_code == 200
        assert rv.data.decode('utf-8') == body
        assert 'application/json' in rv.headers['Content-Type']

    def test_api_serve_xml(self):
        body = '<slideshow><title>Demo slideshow</title></slideshow>'

        # Generate a new route
        with self.app.app_context():
            route = routes_handler.new(
                type_='xml',
                body=body
            )
            path = route.path

        rv = self.client.get('/api/' + path)
        assert rv.status_code == 200
        assert rv.data.decode('utf-8') == body
        assert 'application/xml' in rv.headers['Content-Type']

    def test_api_serve_text(self):
        body = 'Hello world'

        # Generate a new route
        with self.app.app_context():
            route = routes_handler.new(
                type_='text',
                body=body
            )
            path = route.path

        rv = self.client.get('/api/' + path)
        assert rv.status_code == 200
        assert rv.data.decode('utf-8') == body
        assert 'text/html; charset=utf-8' in rv.headers['Content-Type']

    def test_api_serve_no_body(self):
        # Generate a new route
        with self.app.app_context():
            route = routes_handler.new(
                type_=None,
                body=None
            )
            path = route.path

        rv = self.client.get('/api/' + path)
        assert rv.status_code == 200
        # Default body is a Json
        assert json.loads(rv.data.decode(
            'utf-8')) == {'success': True, 'info': 'This is a sample API response.'}
        assert 'application/json' in rv.headers['Content-Type']

    def test_abort_404(self):
        rv = self.client.get('/404')
        assert rv.status_code == 404
