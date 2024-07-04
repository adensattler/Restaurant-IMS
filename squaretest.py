from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import pytz


# load all environmental variables and set them as constants
load_dotenv()
SQUARE_LOCATION_ID = os.getenv('SQUARE_LOCATION_ID')

now_utc = datetime.now(timezone.utc)    # Get the current time in UTC
rfc3339_date = now_utc.isoformat()      # Format the datetime object to an RFC 3339-compliant string
# start_time = date.strftime("%Y-%m-%dT00:00:00Z"),
# end_time = (date + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z"),


client = Client(
    bearer_auth_credentials=BearerAuthCredentials(
      access_token=os.getenv('SQUARE_ACCESS_TOKEN')
    ),
    environment='sandbox')




def list_payments(date):
    # Define the Mountain Time time zone
    mountain_time = pytz.timezone('America/Denver')
    
    # Create datetime objects for the start and end of the day in Mountain Time
    start_time = mountain_time.localize(datetime(date.year, date.month, date.day))
    end_time = start_time + timedelta(days=1)
    
    # Format as RFC 3339 strings with the required format
    start_time_rfc3339 = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_time_rfc3339 = end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    # Insert the colon in the timezone offset
    start_time_rfc3339 = start_time_rfc3339[:-2] + ':' + start_time_rfc3339[-2:]
    end_time_rfc3339 = end_time_rfc3339[:-2] + ':' + end_time_rfc3339[-2:]

    print(start_time_rfc3339, end_time_rfc3339)

    response = client.payments.list_payments(
        location_id = SQUARE_LOCATION_ID,
        begin_time = start_time_rfc3339,
        end_time = end_time_rfc3339,
    )
    return response

def extract_order_ids(payments):
    order_ids = []
    for payment in payments:
        if "order_id" in payment:
            order_ids.append(payment["order_id"])
    return order_ids


date = datetime.now()
result = list_payments(date)
if result.is_success():
  print(result.body)
elif result.is_error():
  print(result.errors)
# Extract all order_id values
order_ids = [payment['order_id'] for payment in result.body['payments']]

print(order_ids)




# result = client.payments.list_payments(
#   begin_time = "2024-06-03T00:00:00-06:00",
#   end_time = "2024-07-04T00:00:00-06:00",
#   location_id = "L0AW4R8GPF7FH"
# )

# if result.is_success():
#   print(result.body)
# elif result.is_error():
#   print(result.errors)











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