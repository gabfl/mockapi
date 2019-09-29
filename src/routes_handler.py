import uuid
from datetime import datetime

from .models import db, RouteModel


def new(type_=None, body='', expiration_date=None):
    """ Create a new route """

    # Create route
    route = RouteModel(
        path=str(uuid.uuid4()),
        type_=type_,
        body=body,
        expiration_date=expiration_date,
    )
    db.session.add(route)
    db.session.commit()

    return route


def cleanup_old_routes():
    """ Delete expired mock apis """

    # Load routes
    routes = RouteModel.query.filter(
        RouteModel.expiration_date < datetime.now()).all()

    for route in routes:
        # Delete route
        db.session.delete(route)

    # Commit
    db.session.commit()
