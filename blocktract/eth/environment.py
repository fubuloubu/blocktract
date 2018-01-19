from .types import (
        address,
        timestamp,
    )


# These instances implement Ethereum environment variables
# They reference some opcodes directly when compiling
class BlkTimestamp(timestamp):
    pass

class TxSender(address):
    pass

class MsgSender(address):
    pass

# So this can get loaded by ../context.py:Context
environment = {}
environment['blk'] = {}
environment['blk']['timestamp'] = BlkTimestamp()
environment['tx'] = {}
environment['tx']['sender'] = TxSender()
environment['msg'] = {}
environment['msg']['sender'] = MsgSender()
