from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from flask import make_response
from flask import session

app = Flask(__name__)

'''
@app.route("/<name>")
def hello(name):
    return f"ie, {escape(name)}"
'''

@app.route('/user/<username>')
def show_user_profile(username):
    return f'{username}\'s profile'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

'''
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('show_user_profile', username='John Doe'))
    print(url_for('static', filename='style.css'))
'''

@app.route('/notimplemented')
def notimplemented():
    abort(404)

@app.route('/redireccionar',)
def redireccionar():
    return redirect(url_for('notimplemented'))

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    app.logger.debug('checkea este login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))