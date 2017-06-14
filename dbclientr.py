#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess
app = Flask(__name__)

@app.route('/todo/api/v1.0/db', methods=['GET'])
def get_tasks():
    p = subprocess.Popen(["sudo", "ovsdb-client", "--format=json", "list-tables"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    return output
if __name__ == '__main__':
    app.run(debug=True)
