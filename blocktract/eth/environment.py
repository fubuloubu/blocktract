from .types import (
        Address,
        Timestamp,
        Timedelta
    )

environment = {}
environment['msg'] = {}
environment['msg']['sender'] = Address
environment['blk'] = {}
environment['blk']['timestamp'] = Timestamp
environment['blk']['timedelta'] = Timedelta
environment['tx'] = {}
environment['tx']['sender'] = Address
