# routes/request.py
from flask import Blueprint, request, jsonify
import re, datetime
import db
from models import Book

request_bp = Blueprint('request', __name__)


def is_valid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return bool(re.fullmatch(regex, email))


@request_bp.route("/request", methods=['POST'])
def post_request():
    req_data = request.get_json()
    email = req_data['email']
    if not is_valid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                'res': f'Error ⛔❌! Book with title {title} is already in library!',
                'status': '404'
            })

    bk = Book(db.getNewId(), True, title, datetime.datetime.now())
    db.insert(bk)
    new_bks = [b.serialize() for b in db.view()]
    
    return jsonify({
        'res': bk.serialize(),
        'status': '200',
        'msg': 'Success creating a new book!👍😀'
    })

@request_bp.route('/request', methods=['GET'])
def get_request():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if content_type == 'application/json':
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all books in library!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': bks,
            'status': '200',
            'msg': 'Success getting all books in library!👍😀',
            'no_of_books': len(bks)
        })

@request_bp.route('/request/<id>', methods=['GET'])
def get_request_id(id):
    req_args = request.view_args
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting book by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': bks,
            'status': '200',
            'msg': 'Success getting book by ID!👍😀',
            'no_of_books': len(bks)
        })

@request_bp.route("/request/<id>", methods=['PUT'])
def put_request():
    req_data = request.get_json()
    availability = req_data['available']
    title = req_data['title']
    the_id = req_data['id']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['id'] == the_id:
            bk = Book(
                the_id, 
                availability, 
                title, 
                datetime.datetime.now()
            )
            db.update(bk)
            new_bks = [b.serialize() for b in db.view()]
            return jsonify({
                'res': bk.serialize(),
                'status': '200',
                'msg': f'Success updating the book titled {title}!👍😀'
            })        
    return jsonify({
        'res': f'Error ⛔❌! Failed to update Book with title: {title}!',
        'status': '404'
    })


@request_bp.route('/request/<id>', methods=['DELETE'])
def delete_request(id):
    req_args = request.view_args
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_bks = [b.serialize() for b in db.view()]
                return jsonify({
                    'res': updated_bks,
                    'status': '200',
                    'msg': 'Success deleting book by ID!👍😀',
                    'no_of_books': len(updated_bks)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No Book ID sent!",
            'res': '',
            'status': '404'
        })