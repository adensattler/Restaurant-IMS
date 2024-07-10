import mysql.connector
from flask import current_app, g
import os
import unicodedata      # for normalizing query names
from dotenv import load_dotenv

load_dotenv()

# Global variable to store the development database connection
_dev_db_connection = None

def get_db():
    global _dev_db_connection

    if current_app:
        if 'db' not in g or not g.db.is_connected():
            g.db = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                user=current_app.config['DB_USERNAME'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_DATABASE']
            )
        return g.db
    else:
        # We're outside a Flask application context (e.g., in development)
        if not _dev_db_connection or not _dev_db_connection.is_connected():
            _dev_db_connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE')
            )
        return _dev_db_connection
    

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        # close the database 
        db.close()

# In your Flask app setup
def init_app(app):
    app.teardown_appcontext(close_db)

# Takes a menu item name and returns its associated ID if it exists in the database
def get_menu_item_id(menu_item_name):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Normalize the input string
    normalized_name = normalize_string(menu_item_name)

    query = "SELECT menu_item_id FROM MenuItems WHERE LOWER(name) = LOWER(%s)"
    cursor.execute(query, (normalized_name, ))
    result = cursor.fetchone()
    cursor.close()
    return result['menu_item_id'] if result else None

def get_menu_item_components(menu_item_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT inventory_item_id, quantity_required 
    FROM MenuItemComponents 
    WHERE menu_item_id = %s
    """
    cursor.execute(query, (menu_item_id,))
    components = cursor.fetchall()
    cursor.close()
    return components

def update_inventory_quantity(inventory_item_id, quantity_used):
    db = get_db()
    cursor = db.cursor()
    query="""
    UPDATE InventoryItems SET stock = stock - %s
    WHERE inventory_item_id = %s
    """
    cursor.execute(query, (quantity_used, inventory_item_id, ))
    db.commit()
    cursor.close()

def add_menu_item_component(menu_item_id, inventory_item_id, quantity_required, unit=None):
    try:
        db = get_db()
        cursor = db.cursor()
        query="""
        INSERT INTO MenuItemComponents (menu_item_id, inventory_item_id, quantity_required, unit)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (menu_item_id, inventory_item_id, quantity_required, unit))
        db.commit()

        print(f"Successfully added new MenuItemComponent with menu_item_id: {menu_item_id}")
        return cursor.lastrowid     # Return the ID of the newly inserted row
    except mysql.connector.Error as err:
        print(f"Error adding MenuItemComponent. {err}")
        db.rollback()
        return None
    finally:
        cursor.close()

def normalize_string(s):
    # First, replace smart quotes with standard quotes
    s = s.replace("’", "'").replace("‘", "'").replace('“', '"').replace('”', '"')

    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def update_inventory(db, orders):
    for order in orders:
        menu_item_name = order['name']
        quantity = order['quantity']
        
        menu_item_id = get_menu_item_id(menu_item_name)
        if menu_item_id is None:
            print(f"Warning: Menu item '{menu_item_name}' not found")
            continue
        
        components = get_menu_item_components(menu_item_id)
        
        for component in components:
            inventory_item_id = component['inventory_item_id']
            quantity_required = component['quantity_required'] * quantity
            
            update_inventory_quantity(inventory_item_id, quantity_required)
    
    print("Inventory updated successfully")


