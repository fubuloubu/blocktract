Globals
=======
Talk about state here, discuss what each does etc.

.. state:: python
  running: bool = False
  duration: timedelta = :null:
  start-time: timestamp = :null:

Inital Conditions
=================
Talk about the initial conditions and what they mean here

If arguments are given, they are mandatory

.. init:: python
  duration = :arg:

Methods
=======
Talk about each method and what it does

This method lets you start the timer

.. start:: python
  start-time = :msg.timestamp:
  running = True

This method allows you to test if the timer has exceeded the duration since start

.. timed-out:: python
  assert running
  return :msg.timestamp: >= start-time + duration
