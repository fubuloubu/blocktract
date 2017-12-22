Timed Auction Contract
=====================

.. import::
  Role from :std:
  Timer from :std:

The owner of an external contract `deed` creates this contract
to run a timed auction for the sale of their asset with a given
starting bid and duration.

.. state::
  deed: Contract (
    owner: Role
  )
  highest-bidder: Role
  timer: Timer
  bid: Ether

NOTE: Generates `deed.address: address, timer.duration: timedelta, bid: Ether` for ABI

.. init::
  deed(:arg[0]:)
  assert deed.owner is :msg.sender:
  timer(:arg[1]:)
  bid = :arg[2]:
  timer.start()

The bidding is allowed from when this contract is deployed,
and is disallowed when the timer has timed out.
If a bid is made that is larger than a previous bid,
the highest bidder is recorded, and the next highest bidder
is refunded

.. bid::
  assert not timer.timed-out()
  assert :msg.value: > bid
  # Give the next highest their bid back
  # NOTE No highest bidder exists the first time
  if highest-bidder is not :null: :
    highest-bidder.transfer(bid)
  # Set the bid value for the next time
  bid = :msg.value:
  highest-bidder = :msg.sender:

When the timer is timed out, the owner of the deed transfers
ownership of the asset to the auction winner, and transfers
the proceeds to their own account.

.. claim::
  deed.owner.reassign(highest-bidder)
  selfdestruct(:msg.sender:)
