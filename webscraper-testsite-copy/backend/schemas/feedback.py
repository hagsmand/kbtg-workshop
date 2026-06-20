"""Feedback validation schema"""
from marshmallow import Schema, fields, validate


class FeedbackSchema(Schema):
    """Schema for validating feedback submissions"""
    
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5, error='Rating must be between 1 and 5'),
        error_messages={
            'required': 'Rating is required',
            'null': 'Rating cannot be null',
            'invalid': 'Rating must be an integer'
        }
    )
    
    comment = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=1000, error='Comment must be between 5 and 1000 characters'),
        error_messages={
            'required': 'Comment is required',
            'null': 'Comment cannot be null'
        }
    )
    
    page = fields.Str(
        validate=validate.Length(max=100, error='Page name must not exceed 100 characters'),
        allow_none=True
    )
    
    email = fields.Email(
        validate=validate.Length(max=255, error='Email must not exceed 255 characters'),
        allow_none=True,
        error_messages={
            'invalid': 'Invalid email format'
        }
    )

# Made with Bob
