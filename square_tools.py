from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import pytz
import logging
import database


# load all environmental variables and set them as constants
load_dotenv()
SQUARE_LOCATION_ID = os.getenv('SQUARE_LOCATION_ID')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = Client(
    bearer_auth_credentials=BearerAuthCredentials(
      access_token=os.getenv('SQUARE_ACCESS_TOKEN')
    ),
    environment='sandbox')

# SQUARE API CALL FUNCTIONS
# -----------------------------------------------------------------------------------------------------------------------
def list_payments(date=None):
    if not SQUARE_LOCATION_ID:
        raise ValueError("SQUARE_LOCATION_ID is not set in the environment variables.")

    try:
        start_time_rfc3339, end_time_rfc3339 = get_start_end_times_today(date)

        response = client.payments.list_payments(
            location_id = SQUARE_LOCATION_ID,
            begin_time = start_time_rfc3339,
            end_time = end_time_rfc3339,
        )

        if response.is_success():
            print(f"Successfully retrieved payments for {start_time_rfc3339} to {end_time_rfc3339}")
            return response.body
        elif response.is_error():
            raise Exception(f"Error in list_payments: {response.errors}")
    except Exception as e:
        print(f"{str(e)}")
        raise

def retrieve_orders(order_ids: list[str]):
    if not SQUARE_LOCATION_ID:
        raise ValueError("SQUARE_LOCATION_ID is not set in the environment variables.")
    
    if not order_ids:
        print("No orders to retrieve.")
        return {"orders": []}  # Return an empty list of orders
    
    try:
        response = client.orders.batch_retrieve_orders(
            body = {
                "location_id": SQUARE_LOCATION_ID,
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


# JSON Parsing Functions
# -----------------------------------------------------------------------------------------------------------------------
def extract_order_ids(response):
    """
    Extract all order_id values from the given Square JSON response.
    Args: response (dict): The JSON response containing payment information.
    Returns: list: A list of all order_id values found in the response.
    """
    order_ids = []
    
    if 'payments' in response:
        for payment in response['payments']:
            if 'order_id' in payment:
                order_ids.append(payment['order_id'])
    return order_ids

def extract_sold_items(response):
    sold_items = []
    for order in response['orders']:
        for item in order['line_items']:
            sold_items.append({
                'name': item['name'],
                'quantity': int(item['quantity'])
            })
    return sold_items
   

# Primary Functions
# -----------------------------------------------------------------------------------------------------------------------
def get_start_end_times_today(date=None, timezone_str='America/Denver'):
    """
    Get the start and end times in RFC 3339 format for the given date and timezone.
    
    Args:
        date (datetime): The date for which to get the start and end times.
        timezone_str (str): The time zone string (default is 'America/Denver').
        
    Returns:
        tuple: A tuple containing the start and end times in RFC 3339 format.
    """
    # Use provided date or current date if none provided
    if date is None:
        date = datetime.now()

    # Define the specified time zone
    timezone = pytz.timezone(timezone_str)
    
    # Create datetime objects for the start of the CURRENT day (midnight) in the specified time zone
    start_time = timezone.localize(datetime(date.year, date.month, date.day))
    
    # Create datetime objects for the start of the NEXT day (midnight) in the specified time zone
    end_time = start_time + timedelta(days=1)
    
    # Format as RFC 3339 strings with the required format
    start_time_rfc3339 = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_time_rfc3339 = end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    # Insert the colon in the timezone offset (strftime %z formats UTC offset as without the colon. ex: -0600)
    start_time_rfc3339 = start_time_rfc3339[:-2] + ':' + start_time_rfc3339[-2:]
    end_time_rfc3339 = end_time_rfc3339[:-2] + ':' + end_time_rfc3339[-2:]
    
    return start_time_rfc3339, end_time_rfc3339


def update_inventory(orders):
    for order in orders:
        menu_item_name = order['name']
        quantity = order['quantity']
        
        # Get menu_item_id
        menu_item_id = database.get_menu_item_id(menu_item_name)
        
        # Get components for this menu item
        components = database.get_menu_item_components(menu_item_id)
        
        for component in components:
            inventory_item_id = component['inventory_item_id']
            quantity_required = component['quantity_required'] * quantity
            
            # Update inventory
            database.update_inventory_quantity(inventory_item_id, quantity_required)



def process_daily_orders():
    # get all the payments that occured today.
    payments_res = list_payments(date = datetime.now())

    # Extract all order_id values from all payments
    order_ids = extract_order_ids(payments_res)
    print(order_ids)

    # Retrieve all item names from every order
    response = retrieve_orders(order_ids)
    order_items = extract_sold_items(response)
    print(order_items)

    # Update the inventory associated with each and every menu item sold
    database.update_inventory(database.getdbDev, order_items)





if __name__ == '__main__':
    process_daily_orders()

    # print(database.get_menu_item_id('Rib Plate'))

    














# result = client.inventory.retrieve_inventory_count(
#   catalog_object_id = "7HOMZTAM7TD67BUTXIGWQXTV",
#   location_ids = SQUARE_LOCATION_ID,
# )

# if result.is_success():
#   print(result.body)
# # elif result.is_error():
# #   print(result.errors)

# elif result.is_error():
#     for error in result.errors:
#         print(error['category'])
#         print(error['code'])
#         print(error['detail'])