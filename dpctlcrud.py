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

@app.route('/todo/api/v1.0/dp', methods=['POST'])
def create_dp():
    if not request.json or not 'dpname' in request.json:
        abort(400)
    dp = {
        'id': dps[-1]['id'] + 1,
        'dpname': request.json['dpname']
    }
    dps.append(dp)
    dpname = str(request.json['dpname'])
    concat = "ovs-dpctl add-dp %s" % (dpname)
    subprocess.call(concat, shell = True)
    return jsonify({'dp': dp}), 201

@app.route('/todo/api/v1.0/delete/<int:dp_id>', methods=['DELETE'])
def delete_dp(dp_id):
    dp = [dp for dp in dps if dp['id'] == dp_id]
    if len(dp) == 0:
        abort(404)
    dpdeletename = str(dp[0]['dpname'])
    dps.remove(dp[0])
    concat = "ovs-dpctl del-dp %s" % (dpdeletename)
    subprocess.call(concat, shell = True)
    p = subprocess.Popen(["sudo","ovs-dpctl","dump-dps"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    return output

@app.route('/todo/api/v1.0/mod/<int:dp_id>', methods=['PUT'])
def update_dp(dp_id):
    dp = [dp for dp in dps if dp['id'] == dp_id]
    if len(dp) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'dpname' in request.json and type(request.json['dpname']) != unicode:
        abort(400)
    dpmodname = str(dp[0]['dpname'])
    concat = "ovs-dpctl del-dp %s" % (dpmodname)
    subprocess.call(concat, shell = True)
    dp[0]['dpname'] = request.json.get('dpname', dp[0]['dpname'])

    dpnewname = str(request.json['dpname'])
    concat2 = "ovs-dpctl add-dp %s" % (dpnewname)
    subprocess.call(concat2, shell = True)

    return jsonify({'dp': dp[0]})

if __name__ == '__main__':
    app.run(debug=True)

