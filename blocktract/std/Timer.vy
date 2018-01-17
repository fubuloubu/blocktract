running: bool
duration: timedelta
start_time: timestamp

# NOTE: '__init__', '__repr__', and '__assign__' are optional,
#       compiler will throw if used when unimplemented.

@private
def __assign__(set_duration: timedelta):
    self.duration = set_duration

@public
def start():
    self.start_time = blk.timestamp
    self.running = True

@public
def reset():
    self.running = False

@public
def active() -> bool:
    return self.running and blk.timestamp <= self.start_time + self.duration
