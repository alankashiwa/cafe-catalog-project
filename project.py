from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, User, Category, Item

from functools import wraps
from flask import session as login_session
import random
import string

# for gconnect
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

app = Flask(__name__)

# Read and store google client id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login/')
def login():
    """ Display login page """
    categories = session.query(Category).all()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', categories=categories, STATE=state)


@app.route('/logout/')
def logout():
    """ Process logout requests """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('mainPage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('mainPage'))


def login_required(f):
    """Decorator function to check user login """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("Please Login!")
            return redirect('/login/')
    return decorated_function


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Login with google+ """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dump('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'apllication/json'
        return response
    # Obtain auth. code
    code = request.data

    # Exchange the code for credential object
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check validity of the access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # Check error in the access token info
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify whether the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if use is already login
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # check user existence/make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect/')
def gdisconnect():
    """ Logout with google + """
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access token is None')
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # NOQA
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                                 'Failed to revoke token for the user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Login with Facebook """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data.decode()
    print('access token received %s ' % access_token)

    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # NOQA
        app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1].decode()

    # User token to get user info from API
    userinfo_url = 'https://graph.facebook.com/v2.1/me'

    # Obtain the key:value for the server access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.1/me?access_token=%s&fields=name,id,email' % token  # NOQA

    http = httplib2.Http()
    result = http.request(url, 'GET')[1].decode()
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # Store the token in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.1/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # NOQA
    http = httplib2.Http()
    result = http.request(url, 'GET')[1].decode()
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """ Logout with facebook """
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # NOQA
    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]
    return "You have been logged out"


@app.route('/')
def mainPage():
    """ Display the main page and lastest items """
    categories = session.query(Category).all()
    # Get the latest 6 items
    items = session.query(Item).order_by(desc(Item.id))[:6]
    return render_template('mainPage.html',
                           categories=categories,
                           items=items)


@app.route('/catalog/<string:category_name>/items/')
def category(category_name):
    """ Display items of the same category """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category.html',
                           categories=categories,
                           category=category,
                           items=items)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item(category_name, item_name):
    """ Display the item detail """
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(name=item_name).one()
    return render_template('item.html',
                           categories=categories,
                           item=item)


@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def createItem():
    """ Display the item creation form """
    categories = session.query(Category).all()
    if request.method == 'POST':
        category = (session.query(Category)
                    .filter_by(name=request.form['category']).one())
        nItem = Item(name=request.form['name'],
                     description=request.form['description'],
                     price=request.form['price'],
                     image_url=request.form['image_url'],
                     category=category,
                     user_id=login_session['user_id'])
        session.add(nItem)
        session.commit()
        flash('New Item: %s Successfully Created' % nItem.name)
        return redirect(url_for('category', category_name=nItem.category.name))
    else:
        return render_template('createItem.html', categories=categories)


@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    """Display the item edition form """
    editedItem = session.query(Item).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    if editedItem.user_id != login_session['user_id']:
        flash("You cannot edit this item!")
        return redirect(url_for('item',
                                category_name=editedItem.category.name,
                                item_name=editedItem.name))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['image_url']:
            editedItem.image_url = request.form['image_url']
        if request.form['category']:
            itemCategoryName = request.form['category']
            editedItem.category = (
                session.query(Category).filter_by(name=itemCategoryName).one()
            )
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('category', category_name=itemCategoryName))
    else:
        return render_template('editItem.html',
                               categories=categories,
                               item=editedItem)


@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    """ Display item deletetion page """
    categories = session.query(Category).all()
    itemToDelete = session.query(Item).filter_by(name=item_name).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash("You cannot delete this item!")
        return redirect(url_for('item',
                                category_name=itemToDelete.category.name,
                                item_name=itemToDelete.name))
    if request.method == 'POST':
        redirectCatName = itemToDelete.category.name
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('category', category_name=redirectCatName))
    else:
        return render_template('deleteItem.html',
                               categories=categories,
                               item=itemToDelete)


# User Helper Functions
def createUser(login_session):
    """ Add user to the db """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """ Get user object """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ Get user id from email address """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON API for the whole catalog
@app.route('/catalog.json')
def catalogJSON():
    """ JSON API for all items """
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])


# JSON API for an arbitrary item
@app.route('/catalog/<string:item_name>/JSON/')
def itemJSON(item_name):
    """ JSON API for a specific item """
    try:
        item = session.query(Item).filter_by(name=item_name).one()
        return jsonify(Item=item.serialize)
    except NoResultFound:
        return "[Error] The item does not exist:  %s" % item_name

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.config['JSON_SORT_KEYS'] = False
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
