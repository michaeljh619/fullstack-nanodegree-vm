#!/usr/bin/python

# imports
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# flask app
app = Flask(__name__)

# set up sql alchemy session
def create_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

# root page
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = create_session()
    restaurant = session.query(Restaurant).get(restaurant_id)
    items = session.query(MenuItem).filter_by(
                          restaurant_id=restaurant_id)
    session.close()
    return render_template('menu.html',restaurant=restaurant,
                           items = items)

# Task 1: Create route for newMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/new",
           methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        session = create_session()
        newItem = MenuItem(name=request.form['name'],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        session.close()
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',
                               restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit",
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # get item to edit
    session = create_session()
    editItem = session.query(MenuItem).get(menu_id)
    # user posted edit
    if request.method == 'POST':
        origName = editItem.name
        if(request.form['name']):
            editItem.name = request.form['name']
        session.add(editItem)
        session.commit()
        flash(origName + " name changed to " + editItem.name)
        session.close()
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    # get request
    else:
        session.close()
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=editItem)

# Task 3: Create route for newMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete",
           methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # get item to delete
    session = create_session()
    deleteItem = session.query(MenuItem).get(menu_id)
    if request.method == 'POST':
        origName = deleteItem.name
        session.delete(deleteItem)
        session.commit()
        flash(origName + " has been deleted.")
        session.close()
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        session.close()
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=deleteItem)

# API (GET Request)
@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
    session = create_session()
    restaurant = session.query(Restaurant).get(restaurant_id)
    items = session.query(MenuItem).filter_by(
                          restaurant_id=restaurant_id).all()
    session.close()
    return jsonify(MenuItems=[i.serialize for i in items])

# API (GET Request)
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def menuJSON(restaurant_id, menu_id):
    session = create_session()
    restaurant = session.query(Restaurant).get(restaurant_id)
    item = session.query(MenuItem).get(menu_id)
    session.close()
    return jsonify(MenuItem=item.serialize)

# if executed as main, which it should be
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # allows code update w/o server restart
    app.debug = True
    # listen on all addresses
    app.run(host='0.0.0.0', port=5000)
