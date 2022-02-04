class Store:
    def __init__(self, displayName, numOfBags):
        self.displayName = displayName # The display name used on the tgtg app
        self.numOfBags = numOfBags # Integer number of bags this store currently has
        # Check if the store is selling
        if(self.numOfBags > 0):
            self.currentlyOpen = True # Boolean variable saying whether this store is currently selling magic bags
        else:
            self.currentlyOpen = False

    # String representation of the class
    def __repr__(self):
        return self.displayName + " with " + str(numOfBags) + " magic bags left."
