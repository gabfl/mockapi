import json
import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from .bootstrap import get_or_create_app
from .models import RouteModel
from . import api_handler, routes_handler


app = get_or_create_app()


@app.route("/")
def hp():
    return render_template('index.html', host_url=request.host_url)


@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')


@app.route("/new", methods=['POST'])
def new():
    # Cleanup old routes
    routes_handler.cleanup_old_routes()

    # Create new API route
    route = api_handler.new()

    return render_template('new.html', host_url=request.host_url, api_path=route.path)


@app.route('/api/<string:route_path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api(route_path):
    # Lookup route
    route = RouteModel.query.filter_by(path=route_path).first()

    # Return 404 if unknown route
    if not route:
        return redirect(url_for('abort_404')), 307

    # Populate new route
    return api_handler.serve(route)


@app.route("/404")
def abort_404():
    return render_template('404.html'), 404
