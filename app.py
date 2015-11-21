from database import db_session
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify
import uuid
import hmac
from oauth2client import client
from hashlib import sha1

from dao.userdao import UserDao
from dao.pagedao import PageDao
from dao.elementdao import ElementDao

import json

# Flask Configuration
app = Flask(__name__)
app.config.from_pyfile('default.conf.py')

# Google OAuth flow object
flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/plus.login',
    redirect_uri='http://127.0.0.1:5000/oauth2callback')


# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    if 'logged_in_user' not in session:
        return redirect("/login")

    curr_user = UserDao.does_user_exist(session['logged_in_user'])
    res = {'api_key': curr_user.api_key}
    return render_template('index.html', res=res)


@app.route('/login', methods=['GET','POST'])
def login():
    res = {'oauth_url': flow.step1_get_authorize_url()}
    return render_template('login.html', res=res)


@app.route('/oauth2callback')
def oauth_success():
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    unique_id = credentials.id_token['sub']
    curr_user = UserDao.does_user_exist(unique_id)
    if not curr_user:
       curr_user = UserDao.add_user(unique_id,"",_generate_key(),credentials.access_token)
    session['logged_in_user'] = curr_user.id
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('logged_in_user', None)
    return redirect('/login')


# API
@app.route('/api/site/<site_id>/pages', methods=['GET','POST'])
def pages(site_id):
    if not _valid_api_key(request):
        return _access_denied()
    if request.method == 'POST':
        return create_page(request, site_id)
    else:
        return show_pages(site_id)

@app.route('/api/site/<site_id>/page/<page_id>', methods=['GET','PUT','DELETE'])
def access_page(site_id,page_id):
    if not _valid_api_key(request):
        return _access_denied()
    if request.method == 'PUT':
        return update_page(page_id)
    if request.method == 'DELETE':
        return delete_page(page_id)
    else:
        return get_page(page_id)


def show_pages(site_id):
    pages = PageDao.get_pages_by_site(site_id)
    data = []
    for page in pages:
        data.append(page.to_dict())
    return _success_message(data,200)


def get_page(page_id):
    curr_page = PageDao.get_page(page_id)
    if curr_page:
        return jsonify(curr_page.to_dict())
    else:
        return _error_message("Invalid Page Id", 400)



def create_page(request, site_id):
    page_json = request.get_json()
    try:
        _verify_page(page_json)
        new_page = PageDao.add_page(page_json['name'], site_id, page_json['order'])
        _add_elements(page_json['elements'], new_page.id)
        ret_page = PageDao.get_page(new_page.id)
        return _success_message(ret_page.to_dict(),201)
    except ValueError as e:
        return _error_message(str(e), 400)


def update_page(page_id):
    page_json = request.get_json()
    try:
        _verify_page(page_json)
        new_page = PageDao.update_page(page_json['name'], page_id, page_json['order'])
        ElementDao.delete_elements(page_id)
        _add_elements(page_json['elements'], page_id)
        ret_page = PageDao.get_page(new_page.id)
        return _success_message(ret_page.to_dict(), 200)
    except ValueError as e:
        return _error_message(str(e), 400)


def delete_page(page_id):
    PageDao.delete_page(page_id)
    return _success_message("Page Deleted", 200)


def _valid_api_key(request):
    if 'Authorization' in request.headers:
        api_key = request.headers['Authorization']
        if UserDao.valid_api_key(api_key):
            return True
    return False


def _add_elements(elements, page_id):
    for i, element in enumerate(elements):
        ElementDao.add_element(element['type'], page_id, i, element['content'])


def _verify_page(json):
    if 'name' not in json:
        raise ValueError("A Page requires a name.")
    if 'order' not in json:
        raise ValueError("A Page requires an order.")


def _access_denied():
    return _error_message("Invalid API Key.", 401)


def _generate_key():
    new_uuid = uuid.uuid4()
    return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()


def _error_message(msg, status):
    return jsonify(status="error", data=msg), status


def _success_message(msg, status):
    return jsonify(status="success", data=msg), status

if __name__ == "__main__":
    app.run(debug=True)


