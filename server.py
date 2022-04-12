import json
from flask import Flask, abort, request
from mock_data import catalog
from config import db
from bson import ObjectId


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

   products = []
    
   cursor = db.products.find({})

   for prod in cursor:
       prod["_id"] = str(prod["_id"])
       products.append(products)


@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json() #return data (payload) from request

    db.products.insert_one(product)
    print(product)

    # fix _id
    product["_id"] = str(product["_id"])

    return json.dumps(product)
    
    
# Get /api/catalog/count -> how many products exist in the catalog
@app.route("/api/catalog/count")
def product_count():
    cursor = db.products.find({})
    count = 0
    for prod in cursor:
        count += 1
    
    return json.dumps(count)


#Get/api/catalog/total => the sum of all products prices
@app.route("/api/catalog/total")
def total_of_catalog():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]
        
    return json.dumps(total)

@app.route("/api/product/<id>")
def get_by_id(id):

    prod = db.products.find_one({"_id": ObjectId(id) })

    if not prod:
          return abort(404, "No product with such ID")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)

    
  

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
    products = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["id"] = str(prod["_id"])
        products.append(prod)
            
    return json.dumps(products)
    

@app.get("/api/someNumbers")
def some_numbers():
 numbers = []

 for num in range(1, 51):

  return json.dumps(numbers)



  #####################################################
  ##############Coupon code end points#################
  #####################################################
  

allCoupons = []


  # create the GET /api/couponCode
  # return all coupons to json list

@app.route("/api/couponCode", methods=["GET"])
def get_coupons():
    coupons = []
    cursor = db.couponCodes.find({})
    for code in cursor:
        code ["_id"] = str(code["_id"])
        coupons.append(code)

    return json.dumps(coupons)

   # create the GET /api/couponCode
   # get the coupon from the request
   # assign an _id
   # and add it to all coupons
   # return the coupon as Json
@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    if not "code" in coupon or not "discount" in coupon:
      return abort(400, "Must contain coupon code.")

    if len(coupon["code"]) < 5:
       return abort(400, "The code should have at least 5 chars.")

    if coupon["discount"] < 5:
       return abort(400, "Invalid discount amount.")

    db.couponCodes.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

@app.route("/api/couponCode/<code>")
def get_coupon_by_code(code):
    coupon = db.couponCodes.find_one({code: ["_id"]})
    if not coupon:
        return abort(404, "Invalid Code")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)




#####################################################
##############User end points#################
#####################################################

@app.route("/api/users", methods=["get"])
def get_users():
    all_users = []
    cursor = db.users.find({})
    for user in cursor:
        user["_id"] = str(user["_id"])
        all_users.append(user)

        return json.dumps(all_users)

@app.route("/api/users", methods=["post"])
def save_user():
    user = request.get_json()
    if not "userName" in user or not "password" in user or not "email" in user:
        return abort(400, "Object must contain, username, email, and password.")
    
    if len(user["userName"]) < 1:
        return abort(400, "Object must contain values for username, email, and password.")

    db.users.insert_one(user)    

    user["_is"] = str(user["_id"])
    return json.dumps(user)

@app.route("/api/users/<email>")
def get_user_by_email(email):
    user = db.users.find_one({"email": email})
    if not user:
        return abort(404, "No user with that email.")

    user["_id"] = str(user["_id"])

    return json.dumps(user)

@app.route("/api/login", methods=["post"])
def validate_user_data():
    data = request.get_json
    
    if not "user" in data:
        return abort (400, "user is required.")
    
    if not "user" in data:
        return abort (400, "password is required")

    user = db.users.find_one({"userName": data["user"], "password": data["password"]})
    if not user:
        abort(401, "No such user with that user name and password.")
    
    user["_id"] = str(user["_id"])
    user.pop("password")

    return json.dumps(user)





app.run(debug=True)