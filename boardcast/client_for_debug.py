from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.sockets.Client import client
from base.GCBChainStructure import Chain, Block


class debug_client(client):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    c = debug_client()
    res = c.send('query for chain')
    res: Chain
    print(res.debugOutputChain())
    print("end")

