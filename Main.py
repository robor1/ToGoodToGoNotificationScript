
import sys
import time
import os
# https://github.com/ahivert/tgtg-python
from tgtg import TgtgClient

# Main loop
def main():
    # check command line for email address
    if(len(sys.argv) == 2):
        email = sys.argv[1]
    else:
        print("USAGE: python3 tgtgApiTestProg.py <email adress of tgtg account>")
        exit(0)

    # Get access to the to good to go account for the api
    client = login(email)

    # Currently will only take stores from the favoutites list
    Stores = getStores(client.get_items())

    # Before moving to the main loop list which stores currently have magic bags

    # annouceAvaiableStores()

    while(True):
        itemsFromFavoutites = client.get_items()

        # Look at each store and see if they have changed
        for item in itemsFromFavoutites:
            # Get the number of magic bags available from this store
            numOfBagsAvailable = item["items_available"]
            # Get this stores id
            currStoreId = item["store"]["store_id"]
            currStore = stores[currStoreId]

            # Check store is closed
            if(currStore.currentlyOpen && numOfBagsAvailable == 0) {
                # announce store is closed
                # Change store to say they are closed
                currStore.currentlyOpen = False
                currStore.numOfBags = 0
            }
            # Check if the store is open
            elif(not currStore.currentlyOpen && numOfBagsAvailable > 0) {
                # Announce store is open
                # Change store to say they are open
                currStore.currentlyOpen = True
                # Update the number of bags available
                currStore.numOfBags = numOfBagsAvailable
            }
        # Run this every minute, does not need to check very often
        time.sleep(60)


def login(email):
    print("Attemping to login into account: " + email)
    # Recieve client credentials by logging in to account via email authentication
    client = TgtgClient(email=email)

    # Loop until users has authenticated their login via their mailbox
    while(True):
        try:
            credentials = client.get_credentials()
        except Exception:
            input("Unable to retrieve your credentials, please check your mailbox and press any key when done")
            continue
        # If the user has authenticated then the loop will break
        break

    # An email will be sent to your account to authenticate that you are trying to log in
    # This will loop until you validate
    # If you have validated the login by email, then this will print an appropriate message
    client = TgtgClient(access_token=credentials["access_token"], refresh_token=credentials["refresh_token"], user_id=credentials["user_id"])
    print("Logged in!")

    return client

def getStores(storeApiCall):
    # Each item on map stored by store_id : <Store object>
    stores = {}

    for sellers in storeApiCall:
        itemsAvailable = sellers["items_available"]
        displayName = sellers["display_name"]
        storeId = sellers["store"]["store_id"]

        stores[storeId] = Store(displayName, itemsAvailable)

    return stores

if __name__ == "__main__":
    main()
