from std import Role, Timer # Multiple imports allowed

# A Deed is any contract that has an `owner` that implements
# the `Role` methods (e.g. `owner

# New AST token 'contract' mapped to 'class'
# unique to external contract definitions
deed: contract # External contract type
    # New AST token 'has' mapped to 'def'
    # unique to external contract definitions
    has owner: Role # Implements methods in type
highest_bidder: Role
timer: Timer
bid: Ether # Special labeled uint256 type


def __init__(deed_address: address, auction_duration: timedelta, starting_bid: Ether):
    # assign Contract address, calling `deed.__assign__(address)`
    # Note: Checks contract at address has required methods implicitly
    self.deed = deed_address # casts ot Deed contract type

    # NOTE: External call to `deed.owner.__repr__()`
    assert self.deed.owner == msg.sender
    
    self.bid = starting_bid

    # Init Timer type, calling 'timer.__init__(timedelta)'
    self.timer = Timer(auction_duration)
    # Start timer, calling 'timer.start()'
    self.timer.start()


def bid():
    assert self.timer.active()
    assert msg.value > self.bid

    # Give the next highest their bid back
    # Note: No highest bidder exists the first time
    if self.highest_bidder != 0x0:
        self.highest_bidder.transfer(self.bid)

    # Set the bid value for the next time
    self.bid = msg.value
    self.highest_bidder = msg.sender


def claim():
    # NOTE: External call to `owner.__assign__(address)` at `deed` address
    self.deed.owner = self.highest_bidder
    selfdestruct(msg.sender)
