from flask import Blueprint, request, Response
import functools

bp = Blueprint('control', __name__, url_prefix='/control')

@bp.route('/move', methods=['POST'])
def move():
    
    print(request.form)
    return Response(status=200)