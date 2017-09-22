from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def mainPage():
    categories = session.query(Category).all()
    return render_template('mainPage.html', categories=categories)

@app.route('/catalog/<string:category_name>/items/')
def category(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category.html',
                            categories=categories,
                            category=category,
                            items=items)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item(category_name, item_name):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(name=item_name).one()
    return render_template('item.html',
                            categories=categories,
                            item=item)

@app.route('/login')
def login():
    return "login"

@app.route('/catalog/<string:category_name>/items/')
def categoryItemList(category_name):
    #return render_template('coffee.html', category=category_name)
    return '/catalog/category_name/items/'



@app.route('/catalog/<string:category_name>/edit/')
def editItem(category_name):
    return '/catalog/category_name/edit/'

@app.route('/catalog/<string:category_name>/delete/')
def deleteItem(category_name):
    return '/catalog/category_name/delete/'

@app.route('/catalog.json')
def json():
    return '/catalog.json'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
