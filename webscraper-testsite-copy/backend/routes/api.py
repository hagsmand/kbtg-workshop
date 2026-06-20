"""
Main API routes - Secure implementation
These endpoints follow security best practices
"""
from flask import Blueprint, request, jsonify
from app import db
from models.contact import Contact
from models.feedback import Feedback
from schemas.contact import ContactSchema
from schemas.feedback import FeedbackSchema
from utils.responses import success_response, error_response
from marshmallow import ValidationError
import json
import os

api_bp = Blueprint('api', __name__)

# Load test sites data
TEST_SITES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_sites.json')
with open(TEST_SITES_PATH, 'r') as f:
    TEST_SITES = json.load(f)


@api_bp.route('/test-sites', methods=['GET'])
def get_test_sites():
    """
    Get all test sites
    
    Returns:
        JSON response with list of test sites
    """
    try:
        return success_response(
            data=TEST_SITES,
            count=len(TEST_SITES)
        )
    except Exception as e:
        return error_response(
            'INTERNAL_ERROR',
            'Failed to retrieve test sites',
            500
        )


@api_bp.route('/test-sites/<int:site_id>', methods=['GET'])
def get_test_site(site_id):
    """
    Get single test site by ID
    
    Args:
        site_id: Test site ID
    
    Returns:
        JSON response with test site data
    """
    try:
        site = next((s for s in TEST_SITES if s['id'] == site_id), None)
        
        if not site:
            return error_response(
                'NOT_FOUND',
                f'Test site with ID {site_id} not found',
                404
            )
        
        return success_response(data=site)
    
    except Exception as e:
        return error_response(
            'INTERNAL_ERROR',
            'Failed to retrieve test site',
            500
        )


@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    """
    Submit contact form (SECURE implementation)
    
    Request Body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Question",
            "message": "Message content"
        }
    
    Returns:
        JSON response with submission confirmation
    """
    schema = ContactSchema()
    
    try:
        # Validate input
        data = schema.load(request.json)
        
        # Create contact record
        contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        
        # Save to database
        db.session.add(contact)
        db.session.commit()
        
        return success_response(
            data=contact.to_dict(),
            message="Contact form submitted successfully. We'll get back to you soon!",
            status_code=201
        )
    
    except ValidationError as e:
        return error_response(
            'VALIDATION_ERROR',
            'Validation failed',
            400,
            e.messages
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            'INTERNAL_ERROR',
            'Failed to submit contact form',
            500
        )


@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback (SECURE implementation)
    
    Request Body:
        {
            "rating": 5,
            "comment": "Great tool!",
            "page": "test-sites",
            "email": "user@example.com"  // optional
        }
    
    Returns:
        JSON response with submission confirmation
    """
    schema = FeedbackSchema()
    
    try:
        # Validate input
        data = schema.load(request.json)
        
        # Create feedback record
        feedback = Feedback(
            rating=data['rating'],
            comment=data['comment'],
            page=data.get('page'),
            email=data.get('email'),
            user_agent=request.headers.get('User-Agent'),
            ip_address=request.remote_addr
        )
        
        # Save to database
        db.session.add(feedback)
        db.session.commit()
        
        return success_response(
            data=feedback.to_dict(),
            message="Thank you for your feedback!",
            status_code=201
        )
    
    except ValidationError as e:
        return error_response(
            'VALIDATION_ERROR',
            'Validation failed',
            400,
            e.messages
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            'INTERNAL_ERROR',
            'Failed to submit feedback',
            500
        )

# Made with Bob
