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

#Get /api/product/cheapest

@app.route("/api/product/cheapest")
def cheapest_product():

    solution = catalog[0]
    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod
            
    return json.dumps(solution)

@app.get("/api/categories")
def unique_categories():
    categories = []
    for prod in catalog:
        category = prod["category"]
        if not category in categories:
            categories.append(category)
    
    return json.dumps(categories)



@app.route("/api/catalog/<category>")
def product_category(category):
    results = []
    for product in catalog:
        if product["category"] == category:
            results.append(product)
            
    return json.dumps(results)
    


app.run(debug=True)