
import sys
import time
import os
from tgtg import TgtgClient

# Taken from: https://www.delftstack.com/howto/python/python-clear-console/
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# Split the string and return the time
def splitTime(timeToSplit):
    # String formatted as '2022-01-19T16:00:00Z'
    # The second half of the split is what we want, also remove the Z from the end of the time
    return timeToSplit.split("T")[1].replace("Z","")

def printCurrentAvaiableItems(apiCallResults):
    numItems = len(apiCallResults)
    if(numItems == 0):
        print("No items available currently.")
    else:
        itemNum = 1
        for keys in apiCallResults:
            # First check if this item from your favourtites list has more than 0 available
            if(keys["items_available"] == 0):
                # If not move to the next item
                continue

            item = keys["item"]
            # # DEBUG
            # for key, value in keys.items() :
            #     print(key, value)
            #     print()
            """
             What we want:
             display_name (str)
             pickip_location {address_line (str)}
             item (name (Str))
             item (description (str))
             item ( average_overall_rating {map average_overall_rating (float)} )
             item (price_including_taxes (minor_units (int), decimals (int)) )
             items_available (int)
             pickup_interval (map start (str), end (str))
            """
            if(item["name"] == ""):
                # Give a default name
                name = "Magic Bag"
            else:
                item["name"]

            # Get the address of where this item is
            pickup_location = keys["pickup_location"]
            address = (pickup_location["address"])["address_line"]

            # Rating value
            average_overall_rating = item["average_overall_rating"]
            # Get overall rating, and round to two decimal places
            rating = str(round(average_overall_rating["average_overall_rating"], 2)) + "/5"

            # Get the price from pence to pounds and
            price_including_taxes = item["price_including_taxes"]
            # Example calculation 300 / 10 * 2
            price = float(price_including_taxes["minor_units"]) / (10 ** float(price_including_taxes["decimals"]))

            # Format the pickup time
            # In the api call, pickup_interval isnt stored within the values of the key item
            pickup_interval = keys["pickup_interval"]
            collectTime = splitTime(pickup_interval["start"]) + "/" + splitTime(pickup_interval["end"])


            # Print the details of the order
            print(str(itemNum) + ". Store: " + keys["display_name"] + "\nAddress: " + address +
             "\nName: " + name
             # + " Description: " + item["description"]
             + "\nRating: " + rating + "\nPrice: £" + str(price) + " Number Available: " + str(keys["items_available"]) + " \nCollection Time: " + collectTime + "\n")

            itemNum = itemNum + 1



# This function will take the api call of either the active orders from an account and print them in a more user friendly fashion
def printActiveOrders(apiCallResults):
    orders = apiCallResults["orders"]
    if(len(orders) == 0):
        print("No orders made currently.\n")
    else:
        # The current order number on the list
        orderNum = 1
        for order in orders:
            """
            what we want from the order map:
            store_name (str)
            store_branch (str)
            state (str)
            quantity (int)
            price_including_taxes (map code (str), minor_units (int), decimals (int))
            pickup_interval (map start (str), end (str))
            """

            # Get the price from pence to pounds and pence
            price_including_taxes = order["price_including_taxes"]
            # Example calculation 300 / 10 * 2
            price = float(price_including_taxes["minor_units"]) / (10 ** float(price_including_taxes["decimals"]))

            # Format the pickup time
            pickup_interval = order["pickup_interval"]
            collectTime = splitTime(pickup_interval["start"]) + "/" + splitTime(pickup_interval["end"])

            # Print the details of the order
            print(str(orderNum) + ". Store: " + order["store_name"] + " Store Branch: " + order["store_branch"] +
             "\nState: " + order["state"] + " Quantity: " + str(order["quantity"]) + " Price: £" + str(price) +
              "\nCollection Time: " + collectTime + "\n")

            orderNum = orderNum + 1

# Main loop

# check command line for email address
if(len(sys.argv) == 2):
    email = sys.argv[1]
else:
    print("USAGE: python3 tgtgApiTestProg.py <email adress of tgtg account>")
    exit(0)

print("Attemping to login into account: " + email)
# Recieve client credentials by logging in to account via email authentication
client = TgtgClient(email=email)

# Loop until users has authenticated their login via their mailbox
while(True):
    input("Press any key when you have completed the email authentication")
    try:
        credentials = client.get_credentials()
    except Exception:
        input("Unable to retrieve your credentials, please check your mailbox")
        continue
    # If the user has authenticated then the loop will break
    break

# An email will be sent to your account to authenticate that you are trying to log in
# This will loop until you validate
# If you have validated the login by email, then this will print an appropriate message
client = TgtgClient(access_token=credentials["access_token"], refresh_token=credentials["refresh_token"], user_id=credentials["user_id"])
print("Logged in!")
# For this test I will list the current active and inactive orders and print this every minute
# this will only take from my favoutites list I believe
while(True):
    clearConsole()
    current_items = client.get_items()
    print("Available items from favourites:")
    printCurrentAvaiableItems(current_items)
    active_orders = client.get_active()
    print("Active Orders:")
    printActiveOrders(active_orders)
    inactive_orders = client.get_inactive()
    # Run this every minute, does not need to check very often
    time.sleep(60)
