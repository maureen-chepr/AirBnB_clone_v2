#!/usr/bin/python3
"""
Flask Web Application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_data(self):
    """
        tears down app context and close db
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ displays all states in the db  """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
