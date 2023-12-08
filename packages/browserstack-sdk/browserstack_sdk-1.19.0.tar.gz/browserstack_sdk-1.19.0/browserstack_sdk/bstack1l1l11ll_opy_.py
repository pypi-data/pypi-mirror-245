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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1ll111l1l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l1ll1_opy_
class bstack1llll1llll_opy_:
    def __init__(self, args, logger, bstack1l111ll1l1_opy_, bstack1l111l1ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1l1_opy_ = bstack1l111ll1l1_opy_
        self.bstack1l111l1ll1_opy_ = bstack1l111l1ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1111l_opy_ = []
        self.bstack1l111l111l_opy_ = None
        self.bstack11l1llll_opy_ = []
        self.bstack1l111l1lll_opy_ = self.bstack1l1llll11_opy_()
        self.bstack1l1llll1_opy_ = -1
    def bstack1l1111ll1_opy_(self, bstack1l111l11ll_opy_):
        self.parse_args()
        self.bstack1l111ll111_opy_()
        self.bstack1l111l1l1l_opy_(bstack1l111l11ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l111ll11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1llll1_opy_ = -1
        if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ඼") in self.bstack1l111ll1l1_opy_:
            self.bstack1l1llll1_opy_ = int(self.bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪල")])
        try:
            bstack1l1111llll_opy_ = [bstackl_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭඾"), bstackl_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ඿"), bstackl_opy_ (u"࠭࠭ࡱࠩව")]
            if self.bstack1l1llll1_opy_ >= 0:
                bstack1l1111llll_opy_.extend([bstackl_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨශ"), bstackl_opy_ (u"ࠨ࠯ࡱࠫෂ")])
            for arg in bstack1l1111llll_opy_:
                self.bstack1l111ll11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l111ll111_opy_(self):
        bstack1l111l111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l111l111l_opy_ = bstack1l111l111l_opy_
        return bstack1l111l111l_opy_
    def bstack11l1l1l1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l1111lll1_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫස"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1111l1ll1_opy_)
    def bstack1l111l1l1l_opy_(self, bstack1l111l11ll_opy_):
        bstack1l1ll111l1_opy_ = Config.get_instance()
        if bstack1l111l11ll_opy_:
            self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧහ"))
            self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"࡙ࠫࡸࡵࡦࠩළ"))
        if bstack1l1ll111l1_opy_.bstack1l111l1l11_opy_():
            self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫෆ"))
            self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"࠭ࡔࡳࡷࡨࠫ෇"))
        self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠧ࠮ࡲࠪ෈"))
        self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭෉"))
        self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵ්ࠫ"))
        self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ෋"))
        if self.bstack1l1llll1_opy_ > 1:
            self.bstack1l111l111l_opy_.append(bstackl_opy_ (u"ࠫ࠲ࡴࠧ෌"))
            self.bstack1l111l111l_opy_.append(str(self.bstack1l1llll1_opy_))
    def bstack1l111ll1ll_opy_(self):
        bstack11l1llll_opy_ = []
        for spec in self.bstack11l1111l_opy_:
            bstack1lll1l1l1_opy_ = [spec]
            bstack1lll1l1l1_opy_ += self.bstack1l111l111l_opy_
            bstack11l1llll_opy_.append(bstack1lll1l1l1_opy_)
        self.bstack11l1llll_opy_ = bstack11l1llll_opy_
        return bstack11l1llll_opy_
    def bstack1l1llll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l111l1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack1l111l1lll_opy_ = False
        return self.bstack1l111l1lll_opy_
    def bstack1llll11111_opy_(self, bstack1l111l1111_opy_, bstack1l1111ll1_opy_):
        bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ෍")] = self.bstack1l111ll1l1_opy_
        multiprocessing.set_start_method(bstackl_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ෎"))
        if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪා") in self.bstack1l111ll1l1_opy_:
            bstack1l1111l11_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll1l11ll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫැ")]):
                bstack1l1111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l111l1111_opy_,
                                                           args=(self.bstack1l111l111l_opy_, bstack1l1111ll1_opy_, bstack1lll1l11ll_opy_)))
            i = 0
            bstack1l111l11l1_opy_ = len(self.bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෑ")])
            for t in bstack1l1111l11_opy_:
                os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪි")] = str(i)
                os.environ[bstackl_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬී")] = json.dumps(self.bstack1l111ll1l1_opy_[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨු")][i % bstack1l111l11l1_opy_])
                i += 1
                t.start()
            for t in bstack1l1111l11_opy_:
                t.join()
            return list(bstack1lll1l11ll_opy_)