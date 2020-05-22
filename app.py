import os, json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Env
# FLASK_APP
# FLASK_DEBUG

basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.debug = True

# Init db 
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(200))
	price = db.Column(db.Float)
	qty = db.Column(db.Integer)

	def __init__(self, name, description, price, qty):
		self.name = name
		self.description = description
		self.price = price
		self.qty = qty

	# def as_dict(self):
	#    return {c.name: getattr(self, c.name) for c in self.__table__.columns}		


# Product Schema
class ProductSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create a produuct
@app.route('/product/', methods=['POST'])
def create_product():
	name = request.json['name']
	description = request.json['description']
	price = request.json['price']
	qty = request.json['qty']

	new_product = Product(name, description, price, qty)
	
	db.session.add(new_product)
	db.session.commit()

	return product_schema.jsonify(new_product)
	# return new_product.as_dict()


# Update a produuct
@app.route('/product/<int:id>/', methods=['PUT'])
def update_product(id):
	product = Product.query.get(id)

	product.name = request.json['name']
	product.description = request.json['description']
	product.price = request.json['price']
	product.qty = request.json['qty']
	
	db.session.add(product)
	db.session.commit()

	return product_schema.jsonify(product)
	# return product.as_dict()


# Delete produuct
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
	product = Product.query.get(id)
	
	db.session.delete(product)
	db.session.commit()

	return product_schema.jsonify(product)
	# return product.as_dict()



# Get all products
@app.route('/product/', methods=['GET'])
def get_products():	
	all_products = Product.query.all()

	result = products_schema.dump(all_products)
	
	return jsonify(result)

	# product_lst = list()
	# for product in all_products:
	# 	product_lst.append(product.as_dict())
	# 	return jsonify(product_lst)


# Get single product
@app.route('/product/<int:id>/', methods=['GET'])
def get_product(id):	
	product = Product.query.get(id)

	return product_schema.jsonify(product)
	# return product.as_dict()	

@app.route('/', methods=['GET'])
def get():
	return jsonify({'msg': 'TEST APi'})


# run server
if __name__=='__main__':
	app.run()