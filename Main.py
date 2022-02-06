
import sys
import time
import datetime
import os
from Store import Store
# https://github.com/ahivert/tgtg-python
from tgtg import TgtgClient
from gtts import gTTS
from playsound import playsound

# Main method
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
    stores = getStores(client.get_items())

    # Before moving to the main loop list which stores currently have magic bags
    for store in stores.values():
        if(store.currentlyOpen):
            annouceAvaiableStore(store)

    # Main loop
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
            if(currStore.currentlyOpen and numOfBagsAvailable == 0):
                # announce store is closed
                announceUnavaiableStore(currStore)
                # Change store to say they are closed
                currStore.currentlyOpen = False
                currStore.numOfBags = 0

            # Check if the store is open
            elif(not currStore.currentlyOpen and numOfBagsAvailable > 0):
                # Announce store is open
                annouceAvaiableStore(currStore)
                # Change store to say they are open
                currStore.currentlyOpen = True
                # Update the number of bags available
                currStore.numOfBags = numOfBagsAvailable
        # Run this every minute, does not need to check very often
        time.sleep(60)

# Deals with logging into the tgtg app to access the api
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

# From an api call get all the stores and put them in store objects within a map
def getStores(storeApiCall):
    # Each item on map stored by store_id : <Store object>
    stores = {}

    for sellers in storeApiCall:
        itemsAvailable = sellers["items_available"]
        displayName = sellers["display_name"]
        storeId = sellers["store"]["store_id"]

        stores[storeId] = Store(displayName, itemsAvailable)

    return stores

# Used to announce when a store has some magic bags
def annouceAvaiableStore(store):
    msg = "Magic bags available at " + store.displayName
    # Print to the terminal with a time stamp
    print(getCurrentTime() + msg)
    announceMsg(msg)

# Used to announce when a store has no more magic bags
def announceUnavaiableStore(store):
    msg = "Store " + store.displayName + "has just run out of magic bags"
    # Print to the terminal with a time stamp
    print(getCurrentTime() + msg)
    announceMsg(msg)

# Return the current time as a str
def getCurrentTime():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S ")

# Annouce a text message using google translate text to speech feature
def announceMsg(msg):
    # Make a gtts object which will speek the msg
    tts = gTTS(msg, lang='en-gb')
    tts.save("annoucement.mp3")
    # playsound function is blocking by default, so won't remove file until its finished playing
    playsound("annoucement.mp3")
    # Since I am lazy I am just going to do this in a simple way for now, creating the mp3 and then deleting it
    os.remove("annoucement.mp3")

if __name__ == "__main__":
    main()
