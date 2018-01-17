running: bool = False
duration: timedelta = 0
start_time: timestamp = 0

# NOTE: '__init__', '__repr__', and '__assign__' are optional,
#       compiler will throw if used when unimplemented.

@private
def __assign__(set_duration: timedelta):
    self.duration = set_duration

@public
def start():
    self.start_time = msg.timestamp
    self.running = True

@public
def reset():
    self.running = False

@public
def active():
    return self.running and msg.timestamp <= start_time + duration
