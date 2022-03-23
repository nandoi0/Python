import json
from flask import Flask, abort
from mock_data import catalog

app = Flask("Server")

@app.route("/")
def home():
    return "Hello from Flask"


@app.route("/me")
def about_me():
    return "Fernando Iribe"




######################################################
################# API ENDPOINTs ######################
######################################################

@app.route("/api/catalog", methods=["get"])
def get_catalog():
    return json.dumps(catalog)


@app.route("/api/catalog", methods=["post"])
def save_product():
    pass

# Get /api/catalog/count -> how many products exist in the catalog
@app.route("/api/catalog/count")
def product_count():
    count = len(catalog)
    return json.dumps(count)


#Get/api/catalog/total => the sum of all products prices
@app.route("/api/catalog/total")
def total_of_catalog():
    total = 0
    for prod in catalog:
        total += prod["price"]
        
    return json.dumps(total)

@app.route("/api/product/<id>")
def get_by_id(id):
    for prod in catalog:
        if prod["_id"] == id:
           return json.dumps(prod)

    
    return abort(404, "No product with such ID")

app.run(debug=True)