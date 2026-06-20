"""Contact model for storing contact form submissions"""
from app import db
from datetime import datetime


class Contact(db.Model):
    """Contact form submission model"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z'
        }
    
    def __repr__(self):
        return f'<Contact {self.id}: {self.name} - {self.subject}>'

# Made with Bob
