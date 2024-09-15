import app.database as database
import json
import re
from openai import OpenAI
from os import environ as env
from urllib.parse import quote_plus, urlencode
from app.helpers import login_required
from authlib.integrations.flask_client import OAuth
from ..extensions import oauth
from flask import Flask, request, session, url_for, redirect, jsonify, Response, stream_with_context, flash, current_app, g, render_template
# from flask_login import login_required, login_user, current_user
from .. import square_tools
from . import base


@base.route('/')
# @login_required
def index():
    db = database.get_db()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT 
        InventoryItems.*, 
        Locations.location_name,
        Units.unit_name,
        Units.unit_abbreviation
    FROM InventoryItems 
    JOIN Locations ON InventoryItems.location_id = Locations.location_id
    LEFT JOIN Units ON InventoryItems.unit_id = Units.unit_id;
    """

    cursor.execute(query)
    inventory = cursor.fetchall()
    cursor.close()
    return render_template('index.html', inventory=inventory)

@base.route('/menu-items')
# @login_required
def menu_items():
    db = database.get_db()
    cursor = db.cursor(dictionary=True)

    # SQL query to fetch menu items along with their associated data
    query = """
    SELECT 
        MenuItems.menu_item_id AS item_id,
        MenuItems.name AS menu_item_name,
        MenuItems.description AS menu_item_description,
        Categories.name AS category_name
    FROM 
        MenuItems
    JOIN 
        Categories ON MenuItems.category_id = Categories.category_id;
    """

    cursor.execute(query)
    menu_items = cursor.fetchall()

    # Fetch inventory items to populate the dropdown
    cursor.execute("SELECT inventory_item_id, name FROM InventoryItems;")
    inventory_items = cursor.fetchall()
    cursor.close()

    # Render the menu items page with the fetched data
    return render_template('menu_items.html', menu_items=menu_items, inventory_items=inventory_items)

@base.route('/get_menu_item_details', methods=['POST'])
def get_menu_item_details():
    menu_item_id = request.form.get('editMenuItemId')
    db = database.get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch menu item details
    cursor.execute("""
        SELECT MenuItems.*, Categories.name AS category_name
        FROM MenuItems
        JOIN Categories ON MenuItems.category_id = Categories.category_id
        WHERE MenuItems.menu_item_id = %s
    """, (menu_item_id,))
    menu_item = cursor.fetchone()

    # Fetch menu item components
    cursor.execute("""
        SELECT InventoryItems.name AS inventory_item_name, InventoryItems.inventory_item_id, MenuItemComponents.quantity_required, MenuItemComponents.unit
        FROM MenuItemComponents
        JOIN InventoryItems ON MenuItemComponents.inventory_item_id = InventoryItems.inventory_item_id
        WHERE MenuItemComponents.menu_item_id = %s
    """, (menu_item_id,))
    components = cursor.fetchall()
    print(components)

    cursor.close()
    return jsonify({
        'menu_item_id': menu_item['menu_item_id'],
        'name': menu_item['name'],
        'description': menu_item['description'],
        'category_name': menu_item['category_name'],
        'components': components
    })

@base.route('/add_menu_item_component', methods=['POST'])
def add_menu_item_component():
    menu_item_id = request.form.get('menu_item_id')
    inventory_item_id = request.form.get('inventory_item_id')
    quantity_required = request.form.get('quantity_required')

    db = database.get_db()
    cursor = db.cursor()

    # Insert new component
    cursor.execute("""
        INSERT INTO MenuItemComponents (menu_item_id, inventory_item_id, quantity_required)
        VALUES (%s, %s, %s)
    """, (menu_item_id, inventory_item_id, quantity_required))

    db.commit()
    cursor.close()

    return jsonify({'status': 'success'})


@base.route('/delete_menu_item_component', methods=['POST'])
def delete_menu_item_component():
    menu_item_id = request.form.get('menu_item_id')
    inventory_item_id = request.form.get('inventory_item_id')
    print(menu_item_id, inventory_item_id)

    db = database.get_db()
    cursor = db.cursor()

    # Delete the component
    cursor.execute("""
        DELETE FROM MenuItemComponents
        WHERE menu_item_id = %s AND inventory_item_id = %s
    """, (menu_item_id, inventory_item_id))

    db.commit()
    cursor.close()

    return jsonify({'status': 'success'})

@base.route('/assistant')
def assistant():
    return render_template('assistant.html')

# Routes For Assistants API Functionality
# -------------------------------------------------------------------------------------
@base.route("/new-thread-id", methods=["GET"])
def new_thread_id():
    client = OpenAI(api_key=env.get("OPENAI_API_KEY"))
    thread = client.beta.threads.create()
    return jsonify({'threadId': thread.id})


@base.route('/add-message', methods=['POST'])
def add_message():
    # adds a message to a provided thread_id
    # will be used just before /stream is called
    data = request.get_json()
    thread_id = data.get('threadId')
    message = data.get('message')

    client = OpenAI(api_key=env.get("OPENAI_API_KEY"))

    # Add user message to thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    
    # Logic to add the message to the specified thread
    return jsonify({'success': True})


# Stream Assitants API Response
@base.route("/stream", methods=["GET"])
def stream():
    client = OpenAI(api_key=env.get("OPENAI_API_KEY"))
    thread_id = request.args.get('threadId')

    # This is added redundancy
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)

    # Reference the Assistants API Docs here for more info on how streaming works:
    # https://platform.openai.com/docs/api-reference/runs/createRun
    def event_generator():
        finished = False
        with client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=env.get("OPENAI_ASSISTANT_ID"),
            stream=True
        ) as stream:
            for event in stream:
                if event.event == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == 'text':
                            data = content.text.value.replace('\n', ' <br> ')
                            yield f"data: {data}\n\n"
                
                elif event.event == "done":
                    finished = True
                    break  
        yield f"data: finish_reason: stop\n\n"

        if finished:
            return

    return Response(stream_with_context(event_generator()), mimetype="text/event-stream")




# @base.route('/send_message', methods=['POST'])
# def send_message():
#     client = OpenAI(api_key=env.get("OPENAI_API_KEY"))
#     data = request.json
#     user_message = data['message']
#     thread_id = data.get('threadId')

#     if not thread_id:
#         thread = client.beta.threads.create()
#         thread_id = thread.id
#     else:
#         thread = client.beta.threads.retrieve(thread_id)

#     # Add user message to thread
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=user_message,
#     )

#     # Run the thread
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread.id,
#         assistant_id=env.get("OPENAI_ASSISTANT_ID"),
#     )

#     if run.status == "failed":
#         return jsonify({"error": f"Run failed: {run.last_error}"}), 500

#     # Retrieve the messages in the thread and get the most recent response
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     new_response = messages.data[0].content[0].text.value

#     # Use re.sub() to remove the matched source tags from the API response
#     # pattern = r'【\d+†source】'
#     # cleaned_response = re.sub(pattern, '', new_response)
#     # Remove the source tags and trailing newlines
#     cleaned_response = re.sub(r'【\d+[:†]\d+†source】', '', new_response)
#     cleaned_response = cleaned_response.strip()
#     print(cleaned_response)

#     return jsonify({"response": cleaned_response, "threadId": thread_id})



@base.route('/removeitem', methods=['POST'])
def remove_item():
    item_id = request.form['item_id']
    print(item_id)

    db = database.get_db()
    cursor = db.cursor()

    # Step 1: Delete associated components from MenuItemComponents
    cursor.execute("""
        DELETE FROM MenuItemComponents WHERE inventory_item_id = %s
    """, (item_id,))

    # Step 2: Delete the inventory item itself
    cursor.execute("""
        DELETE FROM InventoryItems WHERE inventory_item_id = %s
    """, (item_id,))

    db.commit()
    cursor.close()
    return redirect("/")

@base.route('/createitem', methods=['POST'])
def create_item():
    # Ensure name was submitted
    if not request.form.get("itemName"):
        return "must give a name"

    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    item_location = request.form['itemLocation']
    item_GTIN = request.form['itemGTIN']
    item_SKU = request.form['itemSKU']
    item_unit_id = request.form['itemUnit']
    item_weight = request.form['itemWeight'] if request.form['itemWeight'] else None
    item_price = request.form['itemPrice'] if request.form['itemPrice'] else None
    item_stock = request.form['itemStock'] if request.form['itemStock'] else None
    item_low_stock_level = request.form['itemLowStockLevel'] if request.form['itemLowStockLevel'] else None

    db = database.get_db()
    cursor = db.cursor()
    # Execute the SQL query to insert a new item
    insert_query = """
    INSERT INTO InventoryItems (name, description, location_id, GTIN, SKU, unit_id, weight, price, stock, low_stock_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (item_name, item_description, 1, item_GTIN, item_SKU, item_unit_id, item_weight, item_price, item_stock, item_low_stock_level))

    db.commit()
    cursor.close()

    return redirect("/")

@base.route('/updateitem', methods=['POST'])
def update_item():
    # Ensure name was entered!
    if not request.form.get("editItemName"):
        return "Item name is required."

    # collect all data points
    item_id = request.form['editItemID']
    print(item_id)
    item_name = request.form['editItemName']
    item_description = request.form['editItemDescription']
    print(item_description)
    item_location = request.form['editItemLocation']
    item_GTIN = request.form['editItemGTIN']
    item_SKU = request.form['editItemSKU']
    item_unit_id = request.form['editItemUnit']
    item_weight = request.form['editItemWeight'] if request.form['editItemWeight'] else None
    item_price = request.form['editItemPrice'] if request.form['editItemPrice'] else None
    item_stock = request.form['editItemStock'] if request.form['editItemStock'] else None
    item_low_stock_threshold = request.form['editItemLowStockLevel'] if request.form['editItemLowStockLevel'] else None

    db = database.get_db()
    cursor = db.cursor()

    # Execute the SQL query to update the item
    update_query = """
    UPDATE InventoryItems
    SET name = %s,
        description = %s,
        location_id = %s,
        GTIN = %s,
        SKU = %s,
        unit_id = %s,
        weight = %s,
        price = %s,
        stock = %s,
        low_stock_level = %s
    WHERE inventory_item_id = %s
    """
    cursor.execute(update_query, (item_name, item_description, item_location, item_GTIN, item_SKU, item_unit_id, item_weight, item_price, item_stock, item_low_stock_threshold, item_id))
    
    db.commit()
    cursor.close()

    return redirect("/")

@base.route('/get_item_details', methods=['POST'])
def get_item_details():
    item_id = request.form.get('editItemId')
    db = database.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT InventoryItems.*, Units.unit_id, Units.unit_name, Units.unit_abbreviation 
        FROM InventoryItems 
        LEFT JOIN Units ON InventoryItems.unit_id = Units.unit_id 
        WHERE InventoryItems.inventory_item_id = %s
    """, (item_id,))
    item_details = cursor.fetchone()
    cursor.close()
    
    return jsonify(item_details)

@base.route('/restricted')
@login_required
def restricted_page():
    return 'test'        

# Controllers API
@base.route("/test")
def home():
    return json.dumps(session.get("user"), indent=4)


@base.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@base.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("base.callback", _external=True)
    )


@base.route("/logout")
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

# to test this cron route locally
# curl -X POST http://127.0.0.1:5000/cron/process_daily_orders \
#      -H "Content-Type: application/json"
@base.route('/cron/process_daily_orders', methods=['POST'])
def cron_process_daily_orders():
    try:
        square_tools.process_daily_orders()
        # square_tools.check_low_inventory() 
        return jsonify({"status": "success", "message": "Daily orders processed successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@base.route("/temp")
def temp():
    return render_template("datatable.html")
    # return render_template('index.html')
