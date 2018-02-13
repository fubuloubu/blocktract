@public
running: bool
duration: timedelta
start_time: timestamp

Started: __log__()
Reset: __log__()

# NOTE: '__init__', '__repr__', and '__assign__' are optional,
#       compiler will throw if used when unimplemented.

@private
def __assign__(set_duration: timedelta):
    self.duration = set_duration

@public
def start():
    self.start_time = blk.timestamp
    self.running = True
    log.Started() # Generates `timer.Started` receipt

@public
def reset():
    self.running = False
    log.Reset() # Generates `timer.Reset` receipt

@public
@constant
def active() -> bool:
    return self.running and blk.timestamp <= self.start_time + self.duration
