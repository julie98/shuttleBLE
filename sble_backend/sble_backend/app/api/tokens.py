from flask import jsonify

from . import api
from .auth import basic_auth
import time

@api.route('/tokens', methods=['GET'])
@basic_auth.login_required
def get_token():
    start_time = time.time()
    user = basic_auth.current_user()
    token = user.get_token(email=user.values['email'])
    end_time = time.time()
    print(end_time - start_time)
    return jsonify({'token': token})


def revoke_token():
    pass
