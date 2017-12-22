.. state::
  assignee: address

.. init::
  assignee = msg.sender

.. reassign::
  assert :msg.sender: is assignee
  assignee = :arg[0]:
