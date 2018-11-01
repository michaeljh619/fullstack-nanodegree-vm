#!/usr/bin/python

# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# set up sql alchemy session
def create_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

'''
Root Page:
    displays all the restaurants
'''
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    # create sql session
    session = create_session()
    # get restaurants
    restaurants = session.query(Restaurant).all()
    # close sql session
    session.close()
    # return html
    return render_template('restaurants.html', restaurants=restaurants)


'''
New Restaurant Page:
    gives the user an option to create a new restaurant
'''
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        # create sql session
        session = create_session()
        # create new restaurant
        name = request.form['name']
        newR = Restaurant(name=name)
        # add to restaurant table
        session.add(newR)
        session.commit()
        # close sql session
        session.close()
        # redirect
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


'''
Edit Restaurant Page:
    gives the user an option to edit an existing restaurant
'''
@app.route('/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # create sql session
    session = create_session()
    # get restaurant
    restaurant = session.query(Restaurant).get(restaurant_id)
    if request.method == 'POST':
        # update restaurant
        name = request.form['name']
        restaurant.name = name
        # session add/commit
        session.add(restaurant)
        session.commit()
        # close session
        session.close()
        # redirect
        return redirect(url_for('showRestaurants'))
    else:
        session.close()
        return render_template('editRestaurant.html', 
                               restaurant=restaurant)


'''
Delete Restaurant Page:
    gives the user an option to delete an existing restaurant
'''
@app.route('/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # create session
    session = create_session()
    # get restaurant
    restaurant = session.query(Restaurant).get(restaurant_id)
    if request.method == 'POST':
        # delete item
        session.delete(restaurant)
        session.commit()
        session.close()
        # redirect
        return redirect(url_for('showRestaurants'))
    else:
        session.close()
        return render_template('deleteRestaurant.html',
                           restaurant=restaurant)


'''
Show Menu Page:
    shows the menu for a given restaurant
'''
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # get items from database
    session = create_session()
    items = session.query(MenuItem).all()
    # course lists
    appetizers = list()
    entrees = list()
    desserts = list()
    beverages = list()
    # add items to lists
    for i in items:
        if i.course == 'Appetizer':
            appetizers.append(i)
        elif i.course == 'Entree':
            entrees.append(i)
        elif i.course == 'Dessert':
            desserts.append(i)
        else:
            beverages.append(i)
    # send html
    session.close()
    return render_template('menu.html', restaurant=restaurant,
                           appetizers=appetizers, entrees=entrees,
                           desserts=desserts, beverages=beverages)


'''
New Menu Item Page:
    gives the user an option to add a menu item to a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/new',
           methods=['GET','POST'])
def newMenuItem(restaurant_id):
    # set up session
    session = create_session()
    if request.method == 'POST':
        # set up stuff for new item
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        # create item
        newItem = MenuItem(name=name, description=description,
                           price=price, course=course,
                           restaurant_id=restaurant_id)
        # add item
        session.add(newItem)
        session.commit()
        # close & return
        session.close()
        return redirect(url_for('showMenu', 
                                restaurant_id=restaurant_id))
    else:
        # close & return
        session.close()
        return render_template('newMenuItem.html',
                               restaurant_id=restaurant_id)


'''
Edit Menu Item Page:
    gives the user an option to edit a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # get menu item
    session = create_session()
    item = session.query(MenuItem).get(menu_id)
    # post
    if request.method == 'POST':
        # change name
        name = request.form['name']
        item.name = name
        # insert to database
        session.add(item)
        session.commit()
        session.close()
        # redirect
        return redirect(url_for('showMenu', 
                                restaurant_id=restaurant_id))
    # get
    else:
        session.close()
        return render_template('editMenuItem.html', 
                               restaurant_id=restaurant_id,
                               item=item)


'''
Delete Menu Item Page:
    gives the user an option to delete a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # get item
    session = create_session()
    item = session.query(MenuItem).get(menu_id)
    # post
    if request.method == 'POST':
        # delete item
        session.delete(item)
        session.commit()
        session.close()
        # redirect
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))
    # get
    else:
        session.close()
        return render_template('deleteMenuItem.html',
                           restaurant_id=restaurant_id, item=item)

# when run as main, run flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
