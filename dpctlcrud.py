#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess
app = Flask(__name__)

dps = [
        {
                'id': 1,
                'dpname': 'dp_name'
        }
]

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'sti':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/todo/api/v1.0/dp', methods=['GET'])
@auth.login_required
def get_dps():
    return jsonify({'dps': dps})


@app.route('/todo/api/v1.0/dp/<int:dp_id>', methods=['GET'])
def get_dp(dp_id):
    dp = [dp for dp in dps if dp['id'] == dp_id]
    if len(dp) == 0:
        abort(404)
    return jsonify({'dp': dp[0]})


if __name__ == '__main__':
    app.run(debug=True)

