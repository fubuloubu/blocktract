from std import Role
from std import Timer

# Added token 'contract' mapped to 'class'
# unique to contract definitions
#contract Deed:
#    # Added token 'has' mapped to 'def'
#    # unique to contract definitions
#    has owner: Role

# Must define contract type separately
deed: Deed

highest_bidder: Role
timer: Timer
bid: Ether

def __init__(deed_address: address, timer_duration: timedelta, bid: Ether):
    # init Contract type, calling 'deed.__assign__(address)'
    set(self.deed, deed_address)

    # NOTE: External call to 'deed.owner.__repr__()'
    assert get(self.deed.owner) == msg.sender
    
    self.bid = bid

    # Init Timer type, calling 'timer.__init__(timedelta)'
    self.timer = Timer(timer_duration)
    # Start timer, calling 'timer.start()'
    timer.start()

def bid():
    assert self.timer.active()
    assert msg.value > self.bid

    # Give the next highest their bid back
    # NOTE No highest bidder exists the first time
    if self.highest_bidder != 0x0:
        self.highest_bidder.transfer(bid)

    # Set the bid value for the next time
    self.bid = msg.value
    self.highest_bidder = msg.sender

def claim():
    # NOTE: External call to 'deed.owner.__assign__(address)'
    set(self.deed.owner, self.highest_bidder)
    selfdestruct(msg.sender)
