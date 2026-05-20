import json
from datetime import datetime
from __init__ import db


class FoplVolunteerApplication(db.Model):
    __tablename__ = 'fopl_volunteer_applications'

    id           = db.Column(db.Integer,  primary_key=True)
    first_name   = db.Column(db.String(100), nullable=False)
    last_name    = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(255), nullable=False)
    phone        = db.Column(db.String(30),  nullable=True)
    city         = db.Column(db.String(100), nullable=True)
    zip          = db.Column(db.String(20),  nullable=True)
    hours        = db.Column(db.String(20),  nullable=False)
    _days        = db.Column(db.Text,        nullable=True)
    _roles       = db.Column(db.Text,        nullable=True)
    experience   = db.Column(db.Text,        nullable=True)
    why          = db.Column(db.Text,        nullable=False)
    other        = db.Column(db.Text,        nullable=True)
    status       = db.Column(db.String(20),  nullable=False, default='new')
    submitted_at = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, hours, why,
                 phone=None, city=None, zip=None,
                 days=None, roles=None, experience=None, other=None):
        self.first_name = first_name.strip()
        self.last_name  = last_name.strip()
        self.email      = email.strip().lower()
        self.hours      = hours
        self.why        = why.strip()
        self.phone      = (phone or '').strip() or None
        self.city       = (city  or '').strip() or None
        self.zip        = (zip   or '').strip() or None
        self._days      = json.dumps(days  or [])
        self._roles     = json.dumps(roles or [])
        self.experience = (experience or '').strip() or None
        self.other      = (other or '').strip() or None

    def read(self):
        return {
            'id':           self.id,
            'first_name':   self.first_name,
            'last_name':    self.last_name,
            'email':        self.email,
            'phone':        self.phone,
            'city':         self.city,
            'zip':          self.zip,
            'hours':        self.hours,
            'days':         json.loads(self._days  or '[]'),
            'roles':        json.loads(self._roles or '[]'),
            'experience':   self.experience,
            'why':          self.why,
            'other':        self.other,
            'status':       self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
