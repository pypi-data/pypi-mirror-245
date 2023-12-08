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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1l111ll1l1_opy_, bstack1l111l1ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1l1_opy_ = bstack1l111ll1l1_opy_
        self.bstack1l111l1ll1_opy_ = bstack1l111l1ll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1l1ll11l_opy_(bstack1l1111ll11_opy_):
        bstack1l1111l1ll_opy_ = []
        if bstack1l1111ll11_opy_:
            tokens = str(os.path.basename(bstack1l1111ll11_opy_)).split(bstackl_opy_ (u"ࠨ࡟ࠣ෕"))
            camelcase_name = bstackl_opy_ (u"ࠢࠡࠤූ").join(t.title() for t in tokens)
            suite_name, bstack1l1111ll1l_opy_ = os.path.splitext(camelcase_name)
            bstack1l1111l1ll_opy_.append(suite_name)
        return bstack1l1111l1ll_opy_
    @staticmethod
    def bstack1l1111l1l1_opy_(typename):
        if bstackl_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ෗") in typename:
            return bstackl_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥෘ")
        return bstackl_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦෙ")