"""
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
Simple Green environment Lambda function for Blue-Green API deployment demo.
Simplified version focusing on deployment patterns, not production-ready code.

TODO: In a production implementation, consider adding:
- Input validation and error handling
- Correlation ID tracking and X-Ray tracing
- CORS preflight (OPTIONS) handling
- Proper logging and monitoring
- Authentication and authorization
"""

import json
import uuid
from datetime import datetime


def lambda_handler(event, context):
    """Simple Lambda handler for Green environment."""
    
    # Get request details
    http_method = event.get('httpMethod')
    path = event.get('path', '')
    
    # Route requests
    if http_method == 'GET' and path == '/pets':
        return handle_pets()
    elif http_method == 'POST' and path == '/orders':
        return handle_orders(event)
    elif http_method == 'GET' and path == '/health':
        return handle_health()
    else:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Not found"})
        }


def handle_pets():
    """Handle GET /pets requests - returns hardcoded list of pets."""
    pets_data = [
        {
            "id": 1,
            "name": "Max",
            "category": "dog",
            "status": "available"
        },
        {
            "id": 2,
            "name": "Luna",
            "category": "cat",
            "status": "available"
        },
        {
            "id": 3,
            "name": "Rocky",
            "category": "bird",
            "status": "pending"
        },
        {
            "id": 4,
            "name": "Bella",
            "category": "rabbit",
            "status": "available"
        }
    ]
    
    response_data = {
        "environment": "green",
        "version": "v2.0.0",
        "pets": pets_data
    }
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response_data)
    }


def handle_orders(event):
    """Handle POST /orders requests - creates a pet order."""
    # Parse request body
    order_data = json.loads(event.get('body', '{}'))
    
    # Generate confirmation number and timestamp
    confirmation_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    response_data = {
        "confirmationNumber": confirmation_number,
        "environment": "green",
        "version": "v2.0.0",
        "timestamp": timestamp,
        "data": {
            "id": order_data.get('id'),
            "name": order_data.get('name'),
            "status": "ordered"
        }
    }
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response_data)
    }


def handle_health():
    """Handle GET /health requests."""
    health_data = {
        "status": "healthy",
        "environment": "green",
        "version": "v2.0.0"
    }
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(health_data)
    }