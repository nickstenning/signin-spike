from flask import Flask
from flask import abort, make_response, request, render_template

app = Flask(__name__)

CONTENT_HOST = 'content.dev:5000'
SERVICE_HOST = 'service.dev:5000'
SIDEBAR_HOST = 'sidebar.dev:5000'

ALLOWED_CLIENT_ORIGINS = {'http://sidebar.dev:5000'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/debug')
def debug():
    return render_template('debug.html')


@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')


@app.route('/checkauth')
def checkauth():
    if request.host != SERVICE_HOST:
        abort(404)

    client_origin = None
    if request.args['client'] in ALLOWED_CLIENT_ORIGINS:
        client_origin = request.args['client']

    username = request.cookies.get('username')

    return render_template('checkauth.html',
                           client_origin=client_origin,
                           username=username)


@app.route('/login')
def login():
    if request.host != SERVICE_HOST:
        abort(404)

    username = 'fred'
    resp = make_response(render_template('login.html', username=username))
    resp.set_cookie('username', username)
    return resp


@app.route('/logout')
def logout():
    if request.host != SERVICE_HOST:
        abort(404)

    resp = make_response(render_template('logout.html'))
    resp.set_cookie('username', '', expires=0)
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run()
