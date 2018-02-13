# Role composed type
#
# Address type that tracks who can change it
#
# Use via:
#```python
#from std import Role # Uses file name
#
#owner: Role
#
#def foo():
#    self.owner = Role() # calls Role.__init__() using owner as storage
#    # Note: must be initialized before it is used elsewhere
#
#def bar():
#    assert msg.sender is self.owner # calls owner.__repr__()
#    ...
#
#def baz():
#    self.owner = msg.sender # calls owner.__assign__(address)
#    # implicitly checks msg.sender is self.owner
#```

# Instance variables
@public # Creates getter for role variable (e.g. owner.appointee() in above example)
appointee: address

# Set during type init, uses calling context
# Note: can have 0 or more inputs, no outputs
@private
def __init__():
    self.appointee = msg.sender


# Called when instance is called directly
# e.g. `assert msg.sender is self.owner`
# Note: cannot have inputs, only one output
@private
def __repr__() -> address:
    return self.appointee


# Called when instance is assigned to
# e.g. `self.owner = msg.sender
# Note: must have 1 and only 1 input, and no outputs
@private
def __assign__(new_appointee: address):
    assert msg.sender == self.appointee
    self.appointee = new_appointee
