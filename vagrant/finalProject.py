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

'''
Root Page:
    displays all the restaurants
'''
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)


'''
New Restaurant Page:
    gives the user an option to create a new restaurant
'''
@app.route('/restaurant/new')
def newRestaurant():
    return render_template('newRestaurant.html')


'''
Edit Restaurant Page:
    gives the user an option to edit an existing restaurant
'''
@app.route('/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return render_template('editRestaurant.html', restaurant=restaurant)


'''
Delete Restaurant Page:
    gives the user an option to delete an existing restaurant
'''
@app.route('/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return render_template('deleteRestaurant.html', restaurant=restaurant)


'''
Show Menu Page:
    shows the menu for a given restaurant
'''
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # course lists
    appetizers = list()
    entrees = list()
    desserts = list()
    beverages = list()
    # add items to lists
    for i in items:
        if i['course'] == 'Appetizer':
            appetizers.append(i)
        elif i['course'] == 'Entree':
            entrees.append(i)
        elif i['course'] == 'Dessert':
            desserts.append(i)
        else:
            beverages.append(i)
    # send html
    return render_template('menu.html', restaurant=restaurant,
                           appetizers=appetizers, entrees=entrees,
                           desserts=desserts, beverages=beverages)


'''
New Menu Item Page:
    gives the user an option to add a menu item to a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return render_template('newMenuItem.html')


'''
Edit Menu Item Page:
    gives the user an option to edit a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editMenuItem.html', 
                           restaurant=restaurant, item=item)


'''
Delete Menu Item Page:
    gives the user an option to delete a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html',
                           restaurant=restaurant, item=item)

# when run as main, run flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
