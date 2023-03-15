"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"


with app.app_context():
    connect_db(app)
    db.create_all()
 
 
@app.route('/')
def index():
    """Homepage"""   
    return render_template('home.html')


# ###########  API   ################### #
    
@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = [ cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes= cupcakes)

@app.route('/api/cupcakes/<int:cc_id>')
def get_cupcakes(cc_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cc_id)
    return jsonify(cupcake = cupcake.serialize())
    
@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          size=request.json["size"],
                          rating=request.json["rating"],
                          image=request.json["image"] or None )
    db.session.add(new_cupcake)
    db.session.commit()
    resp_json = jsonify(new_cupcake.serialize())
    return (resp_json, 201)

@app.route('/api/cupcakes/<int:cc_id>', methods=["PATCH"])
def update_cupcake(cc_id):
    """Update a cupcake """
    cupcake = Cupcake.query.get_or_404(cc_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cc_id>', methods=["DELETE"])
def delete_cupcake(cc_id):
    """Delete cupcake"""
    cupcake = Cupcake.query.get_or_404(cc_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message= 'deleted')
