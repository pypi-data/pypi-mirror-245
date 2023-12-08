# coding: UTF-8
import sys
bstack111l1_opy_ = sys.version_info [0] == 2
bstack1lllllll_opy_ = 2048
bstack1l11l1_opy_ = 7
def bstackl_opy_ (bstack1l1l11_opy_):
    global bstack11ll11_opy_
    bstack11lll1_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1l1ll1_opy_ = bstack1l1l11_opy_ [:-1]
    bstack1ll1l11_opy_ = bstack11lll1_opy_ % len (bstack1l1ll1_opy_)
    bstack11111ll_opy_ = bstack1l1ll1_opy_ [:bstack1ll1l11_opy_] + bstack1l1ll1_opy_ [bstack1ll1l11_opy_:]
    if bstack111l1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lllllll_opy_ - (bstack11lll_opy_ + bstack11lll1_opy_) % bstack1l11l1_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1lllllll_opy_ - (bstack11lll_opy_ + bstack11lll1_opy_) % bstack1l11l1_opy_) for bstack11lll_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1llll1l_opy_)
import threading
bstack111l1l11l1_opy_ = 1000
bstack111l11l11l_opy_ = 5
bstack111l1l111l_opy_ = 30
bstack111l11llll_opy_ = 2
class bstack111l1l1111_opy_:
    def __init__(self, handler, bstack111l11lll1_opy_=bstack111l1l11l1_opy_, bstack111l11ll1l_opy_=bstack111l11l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l11lll1_opy_ = bstack111l11lll1_opy_
        self.bstack111l11ll1l_opy_ = bstack111l11ll1l_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack111l11ll11_opy_()
    def bstack111l11ll11_opy_(self):
        self.timer = threading.Timer(self.bstack111l11ll1l_opy_, self.bstack111l1l11ll_opy_)
        self.timer.start()
    def bstack111l11l1l1_opy_(self):
        self.timer.cancel()
    def bstack111l11l111_opy_(self):
        self.bstack111l11l1l1_opy_()
        self.bstack111l11ll11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l11lll1_opy_:
                t = threading.Thread(target=self.bstack111l1l11ll_opy_)
                t.start()
                self.bstack111l11l111_opy_()
    def bstack111l1l11ll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack111l11lll1_opy_]
        del self.queue[:self.bstack111l11lll1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack111l11l1l1_opy_()
        while len(self.queue) > 0:
            self.bstack111l1l11ll_opy_()