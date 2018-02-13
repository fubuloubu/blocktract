from std import Role, Timer # Multiple imports allowed

# A Deed is any contract that has an `owner` that implements
# the `Role` methods (e.g. `owner

# Type definition for external contract
# New AST token 'contract' mapped to 'class' unique to external contract definitions
contract Deed: # External contract type
    # New AST token 'has' mapped to 'def' unique to external contract definitions
    has owner: Role # External contract should have all public methods in type

@public
deed: Deed # Must specify separately
@public
highest_bidder: Role
@public
bid: Ether # Special labeled uint256 type

timer: Timer

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


@public
def bid():
    assert self.timer.active()
    assert msg.value > self.bid

    # Give the next highest their bid back
    # Note: No highest bidder exists the first time
    if self.highest_bidder is not 0x0:
        # ^ necessary because `address.transfer(Ether)` fails if address is 0x0
        self.highest_bidder.transfer(self.bid)

    # Set the bid value for the next time
    self.bid = msg.value
    self.highest_bidder = msg.sender


@public
def claim():
    # External call to `owner.__assign__(address)` at `deed` address
    # Note: implicitly checks `owner.assignee is msg.sender` that's why we have no checks
    self.deed.owner = self.highest_bidder
    selfdestruct(msg.sender)
