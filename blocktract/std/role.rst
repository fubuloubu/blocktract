.. state::
  assignee: address

.. init::
  assignee = :arg[0]:

.. reassign::
  assert :msg.sender: is assignee
  assignee = :arg[0]:
