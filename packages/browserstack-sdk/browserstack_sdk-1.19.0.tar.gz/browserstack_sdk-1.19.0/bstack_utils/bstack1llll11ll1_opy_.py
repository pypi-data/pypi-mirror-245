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
class bstack11l111ll1_opy_:
    def __init__(self, handler):
        self._111l111lll_opy_ = None
        self.handler = handler
        self._111l111l11_opy_ = self.bstack111l111l1l_opy_()
        self.patch()
    def patch(self):
        self._111l111lll_opy_ = self._111l111l11_opy_.execute
        self._111l111l11_opy_.execute = self.bstack111l111ll1_opy_()
    def bstack111l111ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._111l111lll_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111l11_opy_.execute = self._111l111lll_opy_
    @staticmethod
    def bstack111l111l1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver