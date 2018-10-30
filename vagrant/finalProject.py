#!/usr/bin/python

# imports
from flask import Flask
app = Flask(__name__)


'''
Root Page:
    displays all the restaurants
'''
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return 'This page will show all my restaurants'


'''
New Restaurant Page:
    gives the user an option to create a new restaurant
'''
@app.route('/restaurant/new')
def newRestaurant():
    return 'This page will be for making a new restaurant'


'''
Edit Restaurant Page:
    gives the user an option to edit an existing restaurant
'''
@app.route('/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return 'This page will be for editing a restaurant'


'''
Delete Restaurant Page:
    gives the user an option to delete an existing restaurant
'''
@app.route('/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'This page will be for deleting a restaurant'


'''
Show Menu Page:
    shows the menu for a given restaurant
'''
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return 'This page is the menu for restaurant ' + str(restaurant_id)


'''
New Menu Item Page:
    gives the user an option to add a menu item to a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return 'Makes a new menu item for restaurant ' + str(restaurant_id)


'''
Edit Menu Item Page:
    gives the user an option to edit a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return 'Edits menu item ' + str(menu_id)


'''
Delete Menu Item Page:
    gives the user an option to delete a menu item from a restaurant
'''
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return 'Deletes menu item ' + str(menu_id)

# when run as main, run flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
