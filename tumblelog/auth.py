from functools import wraps
from flask import request, Response
from tumblelog.models import User



def check_auth(username, password):
	"""fails if no user exist under this username"""
    user = User.objects.get(username=username)
    if user == None:
        return False
    else:
        return user.secret == password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
