from datetime import datetime
from sqlalchemy.exc import IntegrityError
from __init__ import db


class FoplBookInteraction(db.Model):
    """
    FoplBookInteraction
    Tracks books a FOPL user has added to their reading shelf.
    """
    __tablename__ = 'fopl_book_interactions'

    id         = db.Column(db.Integer,    primary_key=True)
    user_id    = db.Column(db.Integer,    db.ForeignKey('fopl_users.id', ondelete='CASCADE'), nullable=False)
    book_id    = db.Column(db.Integer,    db.ForeignKey('fopl_books.id', ondelete='CASCADE'), nullable=False)
    itype      = db.Column(db.String(20), nullable=False, default='read')  # 'read'
    created_at = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', 'itype', name='uq_fopl_user_book_itype'),
    )

    def read(self):
        return {
            'id':         self.id,
            'user_id':    self.user_id,
            'book_id':    self.book_id,
            'type':       self.itype,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()
