from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from __init__ import db
from model.fopl_volunteer import FoplVolunteerApplication
from api.fopl_auth_api import fopl_token_required

fopl_volunteer_api = Blueprint('fopl_volunteer_api', __name__, url_prefix='/api/fopl/volunteer')
api = Api(fopl_volunteer_api)

VALID_STATUSES = {'new', 'reviewed', 'contacted', 'rejected', 'accepted'}


class _Applications(Resource):
    def post(self):
        body = request.get_json() or {}
        first_name = (body.get('first_name') or '').strip()
        last_name  = (body.get('last_name')  or '').strip()
        email      = (body.get('email')      or '').strip()
        hours      = (body.get('hours')      or '').strip()
        why        = (body.get('why')        or '').strip()

        if not all([first_name, last_name, email, hours, why]):
            return {'message': 'Missing required fields.'}, 400

        app = FoplVolunteerApplication(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hours=hours,
            why=why,
            phone=body.get('phone'),
            city=body.get('city'),
            zip=body.get('zip'),
            days=body.get('days'),
            roles=body.get('roles'),
            experience=body.get('experience'),
            other=body.get('other'),
        ).create()

        return jsonify({'id': app.id})

    @fopl_token_required
    def get(self):
        status = request.args.get('status')
        query  = FoplVolunteerApplication.query
        if status:
            query = query.filter_by(status=status)
        apps = query.order_by(FoplVolunteerApplication.submitted_at.desc()).all()
        return jsonify([a.read() for a in apps])


class _Application(Resource):
    @fopl_token_required
    def patch(self, app_id):
        body   = request.get_json() or {}
        status = body.get('status', '')
        if status not in VALID_STATUSES:
            return {'message': 'Invalid status.'}, 400
        app = FoplVolunteerApplication.query.get(app_id)
        if not app:
            return {'message': 'Not found.'}, 404
        app.status = status
        db.session.commit()
        return jsonify({'updated': 1})

    @fopl_token_required
    def delete(self, app_id):
        app = FoplVolunteerApplication.query.get(app_id)
        if not app:
            return {'message': 'Not found.'}, 404
        app.delete()
        return jsonify({'deleted': 1})


api.add_resource(_Applications,  '/applications')
api.add_resource(_Application,   '/applications/<int:app_id>')
