from .types import (
        vyaddress,
        vytimestamp,
    )


# These classes implement Ethereum environment variables
class vyBlkTimestamp(vytimestamp):
    pass

class vyTxSender(vyaddress):
    pass

class vyMsgSender(vyaddress):
    pass

# So this can get loaded by ../context.py:Context
environment = {}
environment['blk'] = {}
environment['blk']['timestamp'] = vyBlkTimestamp()
environment['tx'] = {}
environment['tx']['sender'] = vyTxSender()
environment['msg'] = {}
environment['msg']['sender'] = vyMsgSender()
