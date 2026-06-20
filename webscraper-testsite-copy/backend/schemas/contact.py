"""Contact form validation schema"""
from marshmallow import Schema, fields, validate, ValidationError
import re


class ContactSchema(Schema):
    """Schema for validating contact form submissions"""
    
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100, error='Name must be between 2 and 100 characters'),
            validate.Regexp(
                r'^[a-zA-Z\s\'-]+$',
                error='Name must contain only letters, spaces, hyphens, and apostrophes'
            )
        ],
        error_messages={
            'required': 'Name is required',
            'null': 'Name cannot be null',
            'invalid': 'Invalid name format'
        }
    )
    
    email = fields.Email(
        required=True,
        validate=validate.Length(max=255, error='Email must not exceed 255 characters'),
        error_messages={
            'required': 'Email is required',
            'null': 'Email cannot be null',
            'invalid': 'Invalid email format'
        }
    )
    
    subject = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200, error='Subject must be between 5 and 200 characters'),
        error_messages={
            'required': 'Subject is required',
            'null': 'Subject cannot be null'
        }
    )
    
    message = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=2000, error='Message must be between 10 and 2000 characters'),
        error_messages={
            'required': 'Message is required',
            'null': 'Message cannot be null'
        }
    )

# Made with Bob
