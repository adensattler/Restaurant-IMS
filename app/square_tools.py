from typing import List, Dict, Optional, Tuple
from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client
import os
from datetime import datetime, timezone, timedelta
import pytz
from collections import defaultdict
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

from flask import current_app, g
try:
    from . import database
except ImportError:
    import database

# CONSTANTS
IS_DEV = True


# GET SQUARE CLIENT
# -----------------------------------------------------------------------------------------------------------------------
_dev_square_client = None   # Global variable to store the square client

def get_square_client() -> Client:
    """
    Get or create a Square client instance.
    Returns: A Square client instance.
    """
    global _dev_square_client

    if current_app:
        if 'square_client' not in g:
            g.square_client = Client(
                bearer_auth_credentials=BearerAuthCredentials(
                access_token=os.getenv('SQUARE_ACCESS_TOKEN')
                ),
                environment=current_app.config['SQUARE_ENVIRONMENT']
            )
        return g.square_client
    else:
        if not _dev_square_client:
            _dev_square_client = Client(
                bearer_auth_credentials=BearerAuthCredentials(
                access_token=os.getenv('SQUARE_ACCESS_TOKEN')
                ),
                environment=os.getenv('SQUARE_ENVIRONMENT', 'sandbox')
            )
        return _dev_square_client


# LOW INVENTORY REPORTING FUNCTIONS
# -----------------------------------------------------------------------------------------------------------------------
def check_low_inventory():
    # query database to get all inventory items where 
    low_inventory = database.get_low_stock_items()
    print(low_inventory)

    # parse the response and compile a list off all elements below stock
    if not low_inventory:
        return "No items are currently below their low stock level."

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template('email_template.html')
    html_body = template.render(items=low_inventory)    # Render the HTML template with the low inventory items

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['Subject'] = "Low Stock Items Report"
    msg.attach(MIMEText(html_body, 'html'))         # Attach the HTML content

    # call the send email function with your message!!!
    result = send_low_stock_email(msg)
    print(result)
    
    return "Low stock email sent."

def send_low_stock_email(msg):
    # Email configuration
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("GOOGLE_APP_PASSWORD")

    # Update the message with sender and receiver
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Create SMTP session
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Example for Gmail
            server.starttls()  # Enable security
            server.login(sender_email, password)
            server.send_message(msg)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

def send_low_stock_sms(message_body=None):
    from twilio.rest import Client

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+18669864256',
    body='Hello from Twilio',
    to=os.getenv('TWILIO_TARGET_NUMBER')
    )

    print(message.sid)


# SQUARE API CALL FUNCTIONS
# -----------------------------------------------------------------------------------------------------------------------
def list_payments(date=None) -> Dict[str, List[Dict]]:
    """
    List payments for a given date range. NOTE: THIS IS THE FIRST STEP IN UPDATING INVENTORY
    Args: date (datetime): The date for which to list payments. Defaults to None.
    Returns: Dict[str, List[Dict]]: A dictionary containing a list of payments.
    Raises: Exception if there's an error in retrieving payments.
    """
    client = get_square_client()
    all_payments = []
    cursor = None

    # NOTE: SWITCH DATE RANGE TO TODAY OR YESTERDAY (helps with PROD vs DEV)
    start_time_rfc3339, end_time_rfc3339 = get_daily_start_end_times(date, today=IS_DEV)

    while True:
        response = client.payments.list_payments(
            location_id=os.getenv('SQUARE_LOCATION_ID'),
            begin_time=start_time_rfc3339, 
            end_time=end_time_rfc3339,
            cursor=cursor
        )

        if response.is_success():
            payments = response.body.get('payments', [])
            all_payments.extend(payments)
            print(f"Successfully retrieved {len(payments)} payments for {start_time_rfc3339} to {end_time_rfc3339}")

            cursor = response.body.get('cursor')
            if not cursor:
                break
        elif response.is_error():
            raise Exception(f"Error in list_payments: {response.errors}")

    return {'payments': all_payments}


def retrieve_orders(order_ids: list[str]):
    """
    Retrieve orders by their IDs.
    Args: order_ids (List[str]): A list of order IDs to retrieve.
    Returns: Dict[str, List[Dict]]: A dictionary containing a list of retrieved orders.
    """
    client = get_square_client()
    
    if not order_ids:
        print("No orders to retrieve.")
        return {"orders": []}  # Return an empty list of orders
    
    try:
        response = client.orders.batch_retrieve_orders(
            body = {
                "location_id": os.getenv('SQUARE_LOCATION_ID'),
                "order_ids": order_ids
            }
        )    
        if response.is_success():
            print(f"Successfully retrieved {len(order_ids)} orders")
            return response.body
        elif response.is_error():
            raise Exception(f"Error in retrieve_orders: {response.errors}")
    except Exception as e:
        print(f"{str(e)}")
        raise


# JSON Parsing API Response Functions
# -----------------------------------------------------------------------------------------------------------------------
def extract_order_ids(response: Dict[str, List[Dict]]) -> List[str]:
    """
    Extract all order_id values from a provided Square JSON response (from list_payments).
    Args: response (dict): The JSON response containing payment information.
    Returns: list: A list of all order_id values found in the response.
    """
    order_ids = []
    
    if 'payments' in response:
        for payment in response['payments']:
            if 'order_id' in payment:
                order_ids.append(payment['order_id'])
    print(f"{order_ids}\n")
    return order_ids


def extract_sold_items(response: Dict[str, List[Dict]]) -> List[Dict[str, int]]:
    """
    Extract sold items from the orders response.
    Args: response (Dict[str, List[Dict]]): The response containing order information.
    Returns: List[Dict[str, int]]: A list of dictionaries containing item names and quantities.
    """
    sold_items = []
    for order in response['orders']:
        for item in order['line_items']:
            sold_items.append({
                'name': item['name'],
                'quantity': int(item['quantity'])
            })
    print(f"{sold_items}\n")
    return sold_items
   

# PRIMARY FUNCTIONS
# -----------------------------------------------------------------------------------------------------------------------
def get_daily_start_end_times(date=None, timezone_str='America/Denver', today=False):
    """
    Get the start and end times in RFC 3339 format for the given date and timezone.
    
    Args:
        date (datetime): The date for which to get the start and end times.
        timezone_str (str): The time zone string (default is 'America/Denver').
        
    Returns:
        tuple: A tuple containing the start and end times in RFC 3339 format.
    """
    date = date or datetime.today()
    timezone = pytz.timezone(timezone_str)      # Define the specified time zone

    # Get the start and end times for either yesterday or today (today is for development)
    if today:
        start_time = timezone.localize(datetime(date.year, date.month, date.day))   # Create datetime objects for the start of the CURRENT day (midnight) in the specified time zone
        end_time = start_time + timedelta(days=1)       # Create datetime objects for the start of the NEXT day (midnight) in the specified time zone
    else:
        end_time = timezone.localize(datetime(date.year, date.month, date.day))     # Create datetime object for the start of the NEXT day (midnight) in the specified time zone
        start_time = end_time - timedelta(days=1)           # Create datetime object for the start of the CURRENT day (midnight) in the specified time zone

    # Format as RFC 3339 strings with the required format
    return format_rfc3339(start_time), format_rfc3339(end_time)


def format_rfc3339(dt: datetime) -> str:
    """
    Format a datetime object to RFC 3339 format.
    Args: dt (datetime): The datetime object to format.
    Returns: str: The formatted datetime string in RFC 3339 format.
    """
    formatted = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return f"{formatted[:-2]}:{formatted[-2:]}"         # Insert the colon in the timezone offset (strftime %z formats UTC offset as without the colon. ex: -0600)


def batch_update_inventory(orders):
    """
    Update DATABASE inventory based on a list of orders from extract_sold_items.

    Args: orders (List[Dict[str, int]]): A list of dictionaries containing item names and quantities.
    Returns: List[str]: Nothing if successful! A list of error messages if unsuccessful.
    """
    errors = []

    # combine all orders for each menu item to get a total quantity used for the period
    condensed_orders = defaultdict(int)
    for order in orders:
        condensed_orders[order['name']] += order['quantity']

    # go through each menu item 
    for menu_item_name, quantity_used in condensed_orders.items():
        
        # Retrieve the menu item's id (menu_item_id)
        menu_item_id = database.get_menu_item_id(menu_item_name)
        if menu_item_id is None:
            errors.append(f"Warning: Menu item '{menu_item_name}' not found")
            continue
        
        # Retrieve all components for the current menu item
        components = database.get_menu_item_components(menu_item_id)
        
        for component in components:
            inventory_item_id = component['inventory_item_id']
            total_quantity_used= component['quantity_required'] * quantity_used
            
            # Update inventory
            database.update_inventory_quantity(inventory_item_id, total_quantity_used)
            
    if not errors:
        print("Inventory updated successfully")
    else:
        return errors


# DRIVER FUNCTION
def process_daily_orders():
    """
    Process daily orders, update inventory, and log results. 
    Primary function to update inventory daily.
    """
    print(f"Process daily orders run at {datetime.now()}")

    # get all the payments that occured yesterday (or today for dev testing).
    payments_res = list_payments(date = datetime.now())

    # Extract all order_id values from all payments
    order_ids = extract_order_ids(payments_res)

    # Retrieve all item names from every order
    response = retrieve_orders(order_ids)
    order_items = extract_sold_items(response)

    # Update the inventory associated with each and every menu item sold
    batch_update_inventory(order_items)




# DRIVER
if __name__ == '__main__':
    # print(get_start_end_times_yesterday())
    process_daily_orders()
    check_low_inventory()
    # send_low_stock_email()

    

