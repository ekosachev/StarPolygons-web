import flask
from flask import Flask
from pathlib import Path

from image_generator import generate_polygon

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    n = flask.request.args.get('n')
    m = flask.request.args.get('m')
    r = flask.request.args.get('r')

    path = None
    a = None
    s = None
    p = None
    if not (n is None or m is None or r is None):

        path = f'./cache/{n}-{m}-{float(r)}.png'
        a, s, p = generate_polygon(int(n), int(m), float(r), not Path(path).exists())

    return flask.render_template(
        'index.html',
        path_to_image=f'.{path}',
        a=a,
        s=s,
        p=p
    )

@app.route('/favicon.ico')
def favicon():
    return flask.send_file('./static/spNOBGNOTXT.ico', mimetype='image/x-icon')

"""
A function that sets parameters from a POST request and redirects to a new URL with the parameters.
"""
@app.route('/set_params', methods=['POST'])
def set_params():
    n = int(flask.request.form['n'])
    m = int(flask.request.form['m'])
    r = int(flask.request.form['r'])
    return flask.redirect(f'/?n={n}&m={m}&r={r}')


if __name__ == '__main__':
    app.run()
