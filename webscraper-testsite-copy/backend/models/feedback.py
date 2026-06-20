"""Feedback model for storing user feedback"""
from app import db
from datetime import datetime


class Feedback(db.Model):
    """User feedback model"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    page = db.Column(db.String(100))
    email = db.Column(db.String(255))
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'rating': self.rating,
            'page': self.page,
            'created_at': self.created_at.isoformat() + 'Z'
        }
    
    def __repr__(self):
        return f'<Feedback {self.id}: Rating {self.rating} on {self.page}>'

# Made with Bob
