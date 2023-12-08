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
import sys
class bstack1l1l1l11l1_opy_:
    def __init__(self, handler):
        self._11llll1111_opy_ = sys.stdout.write
        self._11lll1ll1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11lll1llll_opy_
        sys.stdout.error = self.bstack11lll1lll1_opy_
    def bstack11lll1llll_opy_(self, _str):
        self._11llll1111_opy_(_str)
        if self.handler:
            self.handler({bstackl_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ๱"): bstackl_opy_ (u"ࠩࡌࡒࡋࡕࠧ๲"), bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๳"): _str})
    def bstack11lll1lll1_opy_(self, _str):
        self._11lll1ll1l_opy_(_str)
        if self.handler:
            self.handler({bstackl_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๴"): bstackl_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ๵"), bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๶"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11llll1111_opy_
        sys.stderr.write = self._11lll1ll1l_opy_