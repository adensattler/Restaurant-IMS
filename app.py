import database
import json

from flask import Flask, request, session, url_for, redirect, jsonify, flash, current_app, g, render_template
# from flask_login import login_required, login_user, current_user
from os import environ as env
from urllib.parse import quote_plus, urlencode
from helpers import login_required


from authlib.integrations.flask_client import OAuth



app = Flask(__name__)

# load the current_app.config with the vars from .env 
app.config.from_pyfile("config.py")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

@app.route('/')
@login_required
def index():
    db = database.getdb()
    cursor = db.cursor(dictionary=True)

    query = " SELECT Items.*, Locations.location_name FROM Items JOIN Locations ON Items.location_id = Locations.location_id;"

    cursor.execute(query)
    inventory = cursor.fetchall()
    cursor.close()
    return render_template('index.html', inventory=inventory)



@app.route('/removeitem', methods=['POST'])
def remove_item():
    item_id = request.form['item_id']
    print(item_id)

    db = database.getdb()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Items WHERE item_id= %s", (item_id,))
    db.commit()
    cursor.close()
    return redirect("/")

@app.route('/createitem', methods=['POST'])
def create_item():
    # Ensure name was submitted
    if not request.form.get("itemName"):
        return "must give a name"

    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    item_location = request.form['itemLocation']
    item_GTIN = request.form['itemGTIN']
    item_SKU = request.form['itemSKU']
    item_unit = request.form['itemUnit']
    item_weight = request.form['itemWeight'] if request.form['itemWeight'] else None
    item_price = request.form['itemPrice'] if request.form['itemPrice'] else None
    item_stock = request.form['itemStock'] if request.form['itemStock'] else None
    item_low_stock_level = request.form['itemLowStockLevel'] if request.form['itemLowStockLevel'] else None

    db = database.getdb()
    cursor = db.cursor()
    # Execute the SQL query to insert a new item
    insert_query = """
    INSERT INTO Items (name, description, location_id, GTIN, SKU, unit, weight, price, stock, low_stock_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (item_name, item_description, 1, item_GTIN, item_SKU, item_unit, item_weight, item_price, item_stock, item_low_stock_level))

    db.commit()
    cursor.close()

    return redirect("/")

@app.route('/updateitem', methods=['POST'])
def update_item():
    # Ensure name was entered!
    if not request.form.get("editItemName"):
        return "Item name is required."

    # collect a
    item_id = request.form['editItemID']
    item_name = request.form['editItemName']
    item_description = request.form['editItemDescription']
    item_location = request.form['editItemLocation']
    item_GTIN = request.form['editItemGTIN']
    item_SKU = request.form['editItemSKU']
    item_unit = request.form['editItemUnit']
    item_weight = request.form['editItemWeight'] if request.form['editItemWeight'] else None
    item_price = request.form['editItemPrice'] if request.form['editItemPrice'] else None
    item_stock = request.form['editItemStock'] if request.form['editItemStock'] else None
    item_low_stock_threshold = request.form['editItemLowStockLevel'] if request.form['editItemLowStockLevel'] else None

    db = database.getdb()
    cursor = db.cursor()

    # Execute the SQL query to update the item
    update_query = """
    UPDATE Items
    SET name = %s,
        description = %s,
        location_id = %s,
        GTIN = %s,
        SKU = %s,
        unit = %s,
        weight = %s,
        price = %s,
        stock = %s,
        low_stock_level = %s
    WHERE item_id = %s
    """
    cursor.execute(update_query, (item_name, item_description, item_location, item_GTIN, item_SKU, item_unit, item_weight, item_price, item_stock, item_low_stock_threshold, item_id))
    
    db.commit()
    cursor.close()

    return redirect("/")

@app.route('/get_item_details', methods=['POST'])
def get_item_details():
    item_id = request.form.get('editItemId')
    print(item_id)
    db = database.getdb()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Items WHERE Items.item_id = %s", (item_id,))
    item_details = cursor.fetchone()
    cursor.close()
    
    return jsonify(item_details)

@app.route('/restricted')
@login_required
def restricted_page():
    return 'test'        

# Controllers API
@app.route("/test")
def home():
    return json.dumps(session.get("user"), indent=4)


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )



if __name__ == "__main__":
    app.run(debug="True")