from restaurant_appf.models import User, Restaurant, MenuItem
from flask import render_template, url_for, flash, redirect, request, jsonify, session
from restaurant_appf import app, db, bcrypt
from restaurant_appf.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from authlib.integrations.flask_client import OAuth

#---------------------------------------------------------------------------------------------------
#JSON PAGES

"""JSON for restaurants"""
@app.route('/restaurant/JSON')
def restaurant_JSON():

    restaurant = db.session.query(Restaurant).all()

    return jsonify(restaurants=[i.name for i in restaurant])

"""JSON for menus"""
@app.route('/restaurant/<int:restaurant_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_JSON(restaurant_id):

    restaurant = db.session.query(Restaurant).all()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    return jsonify(MenuItems=[i.serialize for i in items])

#---------------------------------------------------------------------------------------------------

#Oauth Setup
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    #userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

github = oauth.register (
    name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)

"""This page will show all my restaurants"""
@app.route('/')
@app.route('/restaurant')
def show_restaurants():    
        
    restaurant = db.session.query(Restaurant).all()        
         
    return render_template('restaurants.html', restaurant = restaurant)      

"""This page will be for making a new restaurant"""
@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():

    if request.method == 'POST':

        new_restaurant = Restaurant(name=request.form['restaurant_name'])
        db.session.add(new_restaurant)
        db.session.commit()
        #flash('New menu item created!')

        return redirect(url_for('show_restaurants'))

    else:

        return render_template('new_restaurant.html')

"""This page will be for editing a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):

    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':

        if request.form['restaurant_name']:

            restaurant.name = request.form['restaurant_name']

        db.session.add(restaurant)
        db.session.commit()
        #flash('Item edited succefully!')

        return redirect(url_for('show_restaurants'))

    else:

        return render_template('edit_restaurant.html', restaurant_id=restaurant_id, r=restaurant)

"""This page will be for deleting a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):

    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':

        db.session.delete(restaurant)
        db.session.commit()
        #flash('Item deleted succefully!')

        return redirect(url_for('show_restaurants'))

    else:

        return render_template('delete_restaurant.html', restaurant_id=restaurant_id, r=restaurant)

"""This page is the menu for a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_menu(restaurant_id):    
    
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu_restaurant.html', restaurant_id=restaurant_id, items=items, restaurant=restaurant)

"""This page is for making a new menu item for a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':

        newItem = MenuItem(name=request.form['menu_name'], price=request.form['menu_price'],
            description=request.form['menu_description'], restaurant_id=restaurant_id)

        session.add(newItem)
        session.commit()
        #flash('New menu item created!')

        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

    else:

        return render_template('new_menu_item.html', restaurant_id=restaurant_id, r=restaurant)

"""This page is for editing a selected menu item for a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):

    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':

        if request.form['menu_name']:

            items.name = request.form['menu_name']

        if request.form['menu_price']:

            items.price = request.form['menu_price']

        if request.form['menu_description']:

            items.description = request.form['menu_description']

        db.session.add(items)
        db.session.commit()
        #flash('Item edited succefully!')

        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

    else:

        return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, i=items, r=restaurant)

"""This page is for deleting a menu item for a selected restaurant"""
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):

    items = db.session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':

        db.session.delete(items)
        db.session.commit()
        #flash('Item deleted succefully!')

        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

    else:

        return render_template('delete_menu_item.html', restaurant_id=restaurant_id, i=items, menu_id=menu_id)

@app.route('/glogin')
def glogin():       
    
    google = oauth.create_client('google')
    redirect_uri = url_for('g_authorize', _external=True)
    
    return google.authorize_redirect(redirect_uri)

@app.route('/glogin/authorize')
def g_authorize():
    
    google = oauth.create_client('google')  
    token = google.authorize_access_token() 
    resp = google.get('userinfo')  
    user_info = resp.json()
    #user = oauth.google.userinfo() 
    session['profile'] = user_info
    session.permanent = False  
    
    user_email = dict(session)['profile']['email']
    user1 = User(name=dict(session)['profile']['name'], email= user_email)
    print(f'\n\n--------------------------------------\n{user_email}\n--------------------------------------\n\n')

    try:
        
        if (db.session.query(User).filter_by(email=user_email).one()) is None:        
        
            db.session.add(user1)
            db.session.commit()
            
    except:
        
        pass        
    
    login_user(user1)  
    print(f'\n\n--------------------------------------\n{current_user.is_active}\n--------------------------------------')
    print(f'\n--------------------------------------\n{current_user.is_authenticated}\n--------------------------------------\n\n')      
    
    return redirect(url_for('show_restaurants'))

@app.route('/github/login')
def github_login():
    
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    
    return github.authorize_redirect(redirect_uri)

@app.route('/github/login/authorize')
def github_authorize():
    
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user')
    print(f"\n{resp}\n")
    
    return redirect(url_for('show_restaurants'))

@app.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    return redirect(url_for('show_restaurants'))