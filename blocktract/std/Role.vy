# Role composed type
#
# Address type that tracks who can change it
#
# Use via:
#```python
#from std import role
#
#owner: role
#
#def foo():
#    self.owner(msg.sender) # calls role.__init__()
#
#def bar():
#    assert msg.sender is self.owner
#    ...
#
#def baz():
#    self.owner = msg.sender # implicitly checks msg.sender is self.owner
#```

# Instance variables
appointee: address

# Set during contract init, takes no args
@private
def __init__():
    self.appointee = msg.sender


# Called when instance is called directly
# e.g. `assert msg.sender is self.owner`

@private
def __repr__() -> address:
    return self.appointee


# Called when instance is assigned to
# e.g. `self.owner = msg.sender

@private
def __assign__(new_appointee: address):
    assert msg.sender == self.appointee
    self.appointee = new_appointee
