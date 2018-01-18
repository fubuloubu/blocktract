from .types import (
        address,
        timestamp,
    )


# These classes implement Ethereum environment variables
class vyBlkTimestamp(timestamp):
    pass

class vyTxSender(address):
    pass

class vyMsgSender(address):
    pass

# So this can get loaded by ../context.py:Context
environment = {}
environment['blk'] = {}
environment['blk']['timestamp'] = vyBlkTimestamp()
environment['tx'] = {}
environment['tx']['sender'] = vyTxSender()
environment['msg'] = {}
environment['msg']['sender'] = vyMsgSender()
