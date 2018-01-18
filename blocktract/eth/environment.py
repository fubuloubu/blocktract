from .types import (
        address,
        timestamp,
        timedelta
    )

environment = {}
environment['msg'] = {}
environment['msg']['sender'] = address()
environment['blk'] = {}
environment['blk']['timestamp'] = timestamp()
environment['blk']['timedelta'] = timedelta()
environment['tx'] = {}
environment['tx']['sender'] = address()
