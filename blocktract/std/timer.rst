# Globals
Talk about state here, discuss what each does etc.

  :_state_:
  running: bool = False
  duration: timedelta = :_null_:
  start-time: timestamp = :_null_:

---

# Inital conditions
Talk about the initial conditions and what they mean here

  :_init_:
  duration = :_arg[0]_:

---

# Methods
Talk about each method and what it does

This method lets you start the timer

  :start:
  start-time = :_msg.timestamp_:
  running = True

This method allows you to test if the timer has exceeded the duration since start

  :timed-out:
  assert running
  return :_msg-timestamp_: >= start-time + duration

