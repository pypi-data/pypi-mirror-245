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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11l1l11l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1l1l11l1_opy_
from bstack_utils.bstack1l11l111l1_opy_ import bstack1l11l1l1l1_opy_, bstack1l11ll111l_opy_, bstack1l11l1lll1_opy_
from bstack_utils.bstack11ll11l11_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1l11ll_opy_, bstack111l11lll_opy_, Result, \
    bstack1l1l11l11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ೰"): [],
        bstackl_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨೱ"): [],
        bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧೲ"): []
    }
    bstack1l1l1l11ll_opy_ = []
    bstack1l11lllll1_opy_ = []
    @staticmethod
    def bstack1l11ll1111_opy_(log):
        if not (log[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬೳ")] and log[bstackl_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭೴")].strip()):
            return
        active = bstack1lll11l1ll_opy_.bstack1l1l1l1ll1_opy_()
        log = {
            bstackl_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ೵"): log[bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭೶")],
            bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ೷"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫ೸"),
            bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೹"): log[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ೺")],
        }
        if active:
            if active[bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪ೻")] == bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ೼"):
                log[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ೽")] = active[bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ೾")]
            elif active[bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ೿")] == bstackl_opy_ (u"ࠪࡸࡪࡹࡴࠨഀ"):
                log[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫഁ")] = active[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬം")]
        bstack1lll11l1ll_opy_.bstack1l11l11111_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l11l11l1l_opy_ = None
        self._1l11llll1l_opy_ = None
        self._1l11ll1l1l_opy_ = OrderedDict()
        self.bstack1l1l111111_opy_ = bstack1l1l1l11l1_opy_(self.bstack1l11ll1111_opy_)
    @bstack1l1l11l11l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l1l11lll1_opy_()
        if not self._1l11ll1l1l_opy_.get(attrs.get(bstackl_opy_ (u"࠭ࡩࡥࠩഃ")), None):
            self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"ࠧࡪࡦࠪഄ"))] = {}
        bstack1l1l1111ll_opy_ = bstack1l11l1lll1_opy_(
                bstack1l11l1ll11_opy_=attrs.get(bstackl_opy_ (u"ࠨ࡫ࡧࠫഅ")),
                name=name,
                bstack1l11llllll_opy_=bstack111l11lll_opy_(),
                file_path=os.path.relpath(attrs[bstackl_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩആ")], start=os.getcwd()) if attrs.get(bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪഇ")) != bstackl_opy_ (u"ࠫࠬഈ") else bstackl_opy_ (u"ࠬ࠭ഉ"),
                framework=bstackl_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬഊ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstackl_opy_ (u"ࠧࡪࡦࠪഋ"), None)
        self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"ࠨ࡫ࡧࠫഌ"))][bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ഍")] = bstack1l1l1111ll_opy_
    @bstack1l1l11l11l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11ll11l1_opy_()
        self._1l11l1l111_opy_(messages)
        for bstack1l11l1l1ll_opy_ in self.bstack1l1l1l11ll_opy_:
            bstack1l11l1l1ll_opy_[bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬഎ")][bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪഏ")].extend(self.store[bstackl_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫഐ")])
            bstack1lll11l1ll_opy_.bstack1l1l11ll1l_opy_(bstack1l11l1l1ll_opy_)
        self.bstack1l1l1l11ll_opy_ = []
        self.store[bstackl_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ഑")] = []
    @bstack1l1l11l11l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l1l111111_opy_.start()
        if not self._1l11ll1l1l_opy_.get(attrs.get(bstackl_opy_ (u"ࠧࡪࡦࠪഒ")), None):
            self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"ࠨ࡫ࡧࠫഓ"))] = {}
        driver = bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨഔ"), None)
        bstack1l11l111l1_opy_ = bstack1l11l1lll1_opy_(
            bstack1l11l1ll11_opy_=attrs.get(bstackl_opy_ (u"ࠪ࡭ࡩ࠭ക")),
            name=name,
            bstack1l11llllll_opy_=bstack111l11lll_opy_(),
            file_path=os.path.relpath(attrs[bstackl_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഖ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1l1ll11l_opy_(attrs.get(bstackl_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഗ"), None)),
            framework=bstackl_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬഘ"),
            tags=attrs[bstackl_opy_ (u"ࠧࡵࡣࡪࡷࠬങ")],
            hooks=self.store[bstackl_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧച")],
            bstack1l1l111lll_opy_=bstack1lll11l1ll_opy_.bstack1l1l11l1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstackl_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦഛ").format(bstackl_opy_ (u"ࠥࠤࠧജ").join(attrs[bstackl_opy_ (u"ࠫࡹࡧࡧࡴࠩഝ")]), name) if attrs[bstackl_opy_ (u"ࠬࡺࡡࡨࡵࠪഞ")] else name
        )
        self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"࠭ࡩࡥࠩട"))][bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪഠ")] = bstack1l11l111l1_opy_
        threading.current_thread().current_test_uuid = bstack1l11l111l1_opy_.bstack1l11ll1ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstackl_opy_ (u"ࠨ࡫ࡧࠫഡ"), None)
        self.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪഢ"), bstack1l11l111l1_opy_)
    @bstack1l1l11l11l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l1l111111_opy_.reset()
        bstack1l111lll1l_opy_ = bstack1l11l1llll_opy_.get(attrs.get(bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪണ")), bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬത"))
        self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"ࠬ࡯ࡤࠨഥ"))][bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩദ")].stop(time=bstack111l11lll_opy_(), duration=int(attrs.get(bstackl_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬധ"), bstackl_opy_ (u"ࠨ࠲ࠪന"))), result=Result(result=bstack1l111lll1l_opy_, exception=attrs.get(bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪഩ")), bstack1l1l1l1111_opy_=[attrs.get(bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫപ"))]))
        self.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ഫ"), self._1l11ll1l1l_opy_[attrs.get(bstackl_opy_ (u"ࠬ࡯ࡤࠨബ"))][bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩഭ")], True)
        self.store[bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫമ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l1l11l11l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l1l11lll1_opy_()
        current_test_id = bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪയ"), None)
        bstack1l1l11l111_opy_ = current_test_id if bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫര"), None) else bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭റ"), None)
        if attrs.get(bstackl_opy_ (u"ࠫࡹࡿࡰࡦࠩല"), bstackl_opy_ (u"ࠬ࠭ള")).lower() in [bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬഴ"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩവ")]:
            hook_type = bstack1l1l111ll1_opy_(attrs.get(bstackl_opy_ (u"ࠨࡶࡼࡴࡪ࠭ശ")), bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ഷ"), None))
            hook_name = bstackl_opy_ (u"ࠪࡿࢂ࠭സ").format(attrs.get(bstackl_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫഹ"), bstackl_opy_ (u"ࠬ࠭ഺ")))
            if hook_type in [bstackl_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎ഻ࠪ"), bstackl_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎ഼ࠪ")]:
                hook_name = bstackl_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩഽ").format(bstack1l1l1ll1l1_opy_.get(hook_type), attrs.get(bstackl_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩാ"), bstackl_opy_ (u"ࠪࠫി")))
            bstack1l11lll11l_opy_ = bstack1l11ll111l_opy_(
                bstack1l11l1ll11_opy_=bstack1l1l11l111_opy_ + bstackl_opy_ (u"ࠫ࠲࠭ീ") + attrs.get(bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪു"), bstackl_opy_ (u"࠭ࠧൂ")).lower(),
                name=hook_name,
                bstack1l11llllll_opy_=bstack111l11lll_opy_(),
                file_path=os.path.relpath(attrs.get(bstackl_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧൃ")), start=os.getcwd()),
                framework=bstackl_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧൄ"),
                tags=attrs[bstackl_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ൅")],
                scope=RobotHandler.bstack1l1l1ll11l_opy_(attrs.get(bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪെ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11lll11l_opy_.bstack1l11ll1ll1_opy_()
            threading.current_thread().current_hook_id = bstack1l1l11l111_opy_ + bstackl_opy_ (u"ࠫ࠲࠭േ") + attrs.get(bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪൈ"), bstackl_opy_ (u"࠭ࠧ൉")).lower()
            self.store[bstackl_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫൊ")] = [bstack1l11lll11l_opy_.bstack1l11ll1ll1_opy_()]
            if bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬോ"), None):
                self.store[bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ൌ")].append(bstack1l11lll11l_opy_.bstack1l11ll1ll1_opy_())
            else:
                self.store[bstackl_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴ്ࠩ")].append(bstack1l11lll11l_opy_.bstack1l11ll1ll1_opy_())
            if bstack1l1l11l111_opy_:
                self._1l11ll1l1l_opy_[bstack1l1l11l111_opy_ + bstackl_opy_ (u"ࠫ࠲࠭ൎ") + attrs.get(bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪ൏"), bstackl_opy_ (u"࠭ࠧ൐")).lower()] = { bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ൑"): bstack1l11lll11l_opy_ }
            bstack1lll11l1ll_opy_.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ൒"), bstack1l11lll11l_opy_)
        else:
            bstack1l1l1l1l1l_opy_ = {
                bstackl_opy_ (u"ࠩ࡬ࡨࠬ൓"): uuid4().__str__(),
                bstackl_opy_ (u"ࠪࡸࡪࡾࡴࠨൔ"): bstackl_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪൕ").format(attrs.get(bstackl_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬൖ")), attrs.get(bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫൗ"), bstackl_opy_ (u"ࠧࠨ൘"))) if attrs.get(bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭൙"), []) else attrs.get(bstackl_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ൚")),
                bstackl_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ൛"): attrs.get(bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩ൜"), []),
                bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ൝"): bstack111l11lll_opy_(),
                bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭൞"): bstackl_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨൟ"),
                bstackl_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ൠ"): attrs.get(bstackl_opy_ (u"ࠩࡧࡳࡨ࠭ൡ"), bstackl_opy_ (u"ࠪࠫൢ"))
            }
            if attrs.get(bstackl_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬൣ"), bstackl_opy_ (u"ࠬ࠭൤")) != bstackl_opy_ (u"࠭ࠧ൥"):
                bstack1l1l1l1l1l_opy_[bstackl_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ൦")] = attrs.get(bstackl_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ൧"))
            if not self.bstack1l11lllll1_opy_:
                self._1l11ll1l1l_opy_[self._1l11l11lll_opy_()][bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൨")].add_step(bstack1l1l1l1l1l_opy_)
                threading.current_thread().current_step_uuid = bstack1l1l1l1l1l_opy_[bstackl_opy_ (u"ࠪ࡭ࡩ࠭൩")]
            self.bstack1l11lllll1_opy_.append(bstack1l1l1l1l1l_opy_)
    @bstack1l1l11l11l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11ll11l1_opy_()
        self._1l11l1l111_opy_(messages)
        current_test_id = bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭൪"), None)
        bstack1l1l11l111_opy_ = current_test_id if current_test_id else bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ൫"), None)
        bstack1l11l111ll_opy_ = bstack1l11l1llll_opy_.get(attrs.get(bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭൬")), bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ൭"))
        bstack1l111lllll_opy_ = attrs.get(bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ൮"))
        if bstack1l11l111ll_opy_ != bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൯") and not attrs.get(bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ൰")) and self._1l11l11l1l_opy_:
            bstack1l111lllll_opy_ = self._1l11l11l1l_opy_
        bstack1l11lll1ll_opy_ = Result(result=bstack1l11l111ll_opy_, exception=bstack1l111lllll_opy_, bstack1l1l1l1111_opy_=[bstack1l111lllll_opy_])
        if attrs.get(bstackl_opy_ (u"ࠫࡹࡿࡰࡦࠩ൱"), bstackl_opy_ (u"ࠬ࠭൲")).lower() in [bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ൳"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ൴")]:
            bstack1l1l11l111_opy_ = current_test_id if current_test_id else bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ൵"), None)
            if bstack1l1l11l111_opy_:
                bstack1l1l11llll_opy_ = bstack1l1l11l111_opy_ + bstackl_opy_ (u"ࠤ࠰ࠦ൶") + attrs.get(bstackl_opy_ (u"ࠪࡸࡾࡶࡥࠨ൷"), bstackl_opy_ (u"ࠫࠬ൸")).lower()
                self._1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ൹")].stop(time=bstack111l11lll_opy_(), duration=int(attrs.get(bstackl_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫൺ"), bstackl_opy_ (u"ࠧ࠱ࠩൻ"))), result=bstack1l11lll1ll_opy_)
                bstack1lll11l1ll_opy_.bstack1l11l1ll1l_opy_(bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪർ"), self._1l11ll1l1l_opy_[bstack1l1l11llll_opy_][bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬൽ")])
        else:
            bstack1l1l11l111_opy_ = current_test_id if current_test_id else bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬൾ"), None)
            if bstack1l1l11l111_opy_ and len(self.bstack1l11lllll1_opy_) == 1:
                current_step_uuid = bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨൿ"), None)
                self._1l11ll1l1l_opy_[bstack1l1l11l111_opy_][bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ඀")].bstack1l11lll111_opy_(current_step_uuid, duration=int(attrs.get(bstackl_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫඁ"), bstackl_opy_ (u"ࠧ࠱ࠩං"))), result=bstack1l11lll1ll_opy_)
            else:
                self.bstack1l1l1lll11_opy_(attrs)
            self.bstack1l11lllll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstackl_opy_ (u"ࠨࡪࡷࡱࡱ࠭ඃ"), bstackl_opy_ (u"ࠩࡱࡳࠬ඄")) == bstackl_opy_ (u"ࠪࡽࡪࡹࠧඅ"):
                return
            self.messages.push(message)
            bstack1l1l1l111l_opy_ = []
            if bstack1lll11l1ll_opy_.bstack1l1l1l1ll1_opy_():
                bstack1l1l1l111l_opy_.append({
                    bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧආ"): bstack111l11lll_opy_(),
                    bstackl_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඇ"): message.get(bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඈ")),
                    bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ඉ"): message.get(bstackl_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧඊ")),
                    **bstack1lll11l1ll_opy_.bstack1l1l1l1ll1_opy_()
                })
                if len(bstack1l1l1l111l_opy_) > 0:
                    bstack1lll11l1ll_opy_.bstack1l11l11111_opy_(bstack1l1l1l111l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lll11l1ll_opy_.bstack1l1l11111l_opy_()
    def bstack1l1l1lll11_opy_(self, bstack1l1l1111l1_opy_):
        if not bstack1lll11l1ll_opy_.bstack1l1l1l1ll1_opy_():
            return
        kwname = bstackl_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨඋ").format(bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪඌ")), bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩඍ"), bstackl_opy_ (u"ࠬ࠭ඎ"))) if bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫඏ"), []) else bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඐ"))
        error_message = bstackl_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢඑ").format(kwname, bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩඒ")), str(bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඓ"))))
        bstack1l1l1l1lll_opy_ = bstackl_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥඔ").format(kwname, bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬඕ")))
        bstack1l1l1ll1ll_opy_ = error_message if bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඖ")) else bstack1l1l1l1lll_opy_
        bstack1l1l1ll111_opy_ = {
            bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ඗"): self.bstack1l11lllll1_opy_[-1].get(bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ඘"), bstack111l11lll_opy_()),
            bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ඙"): bstack1l1l1ll1ll_opy_,
            bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩක"): bstackl_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪඛ") if bstack1l1l1111l1_opy_.get(bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬග")) == bstackl_opy_ (u"࠭ࡆࡂࡋࡏࠫඝ") else bstackl_opy_ (u"ࠧࡊࡐࡉࡓࠬඞ"),
            **bstack1lll11l1ll_opy_.bstack1l1l1l1ll1_opy_()
        }
        bstack1lll11l1ll_opy_.bstack1l11l11111_opy_([bstack1l1l1ll111_opy_])
    def _1l11l11lll_opy_(self):
        for bstack1l11l1ll11_opy_ in reversed(self._1l11ll1l1l_opy_):
            bstack1l11l1111l_opy_ = bstack1l11l1ll11_opy_
            data = self._1l11ll1l1l_opy_[bstack1l11l1ll11_opy_][bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫඟ")]
            if isinstance(data, bstack1l11ll111l_opy_):
                if not bstackl_opy_ (u"ࠩࡈࡅࡈࡎࠧච") in data.bstack1l1l11ll11_opy_():
                    return bstack1l11l1111l_opy_
            else:
                return bstack1l11l1111l_opy_
    def _1l11l1l111_opy_(self, messages):
        try:
            bstack1l11ll1l11_opy_ = BuiltIn().get_variable_value(bstackl_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤඡ")) in (bstack1l1l11l1l1_opy_.DEBUG, bstack1l1l11l1l1_opy_.TRACE)
            for message, bstack1l11ll1lll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬජ"))
                level = message.get(bstackl_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫඣ"))
                if level == bstack1l1l11l1l1_opy_.FAIL:
                    self._1l11l11l1l_opy_ = name or self._1l11l11l1l_opy_
                    self._1l11llll1l_opy_ = bstack1l11ll1lll_opy_.get(bstackl_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢඤ")) if bstack1l11ll1l11_opy_ and bstack1l11ll1lll_opy_ else self._1l11llll1l_opy_
        except:
            pass
    @classmethod
    def bstack1l11l1ll1l_opy_(self, event: str, bstack1l1l111l1l_opy_: bstack1l11l1l1l1_opy_, bstack1l111lll11_opy_=False):
        if event == bstackl_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩඥ"):
            bstack1l1l111l1l_opy_.set(hooks=self.store[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬඦ")])
        if event == bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪට"):
            event = bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඨ")
        if bstack1l111lll11_opy_:
            bstack1l1l111l11_opy_ = {
                bstackl_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨඩ"): event,
                bstack1l1l111l1l_opy_.bstack1l11l11ll1_opy_(): bstack1l1l111l1l_opy_.bstack1l1l1l1l11_opy_(event)
            }
            self.bstack1l1l1l11ll_opy_.append(bstack1l1l111l11_opy_)
        else:
            bstack1lll11l1ll_opy_.bstack1l11l1ll1l_opy_(event, bstack1l1l111l1l_opy_)
class Messages:
    def __init__(self):
        self._1l111llll1_opy_ = []
    def bstack1l1l11lll1_opy_(self):
        self._1l111llll1_opy_.append([])
    def bstack1l11ll11l1_opy_(self):
        return self._1l111llll1_opy_.pop() if self._1l111llll1_opy_ else list()
    def push(self, message):
        self._1l111llll1_opy_[-1].append(message) if self._1l111llll1_opy_ else self._1l111llll1_opy_.append([message])
class bstack1l1l11l1l1_opy_:
    FAIL = bstackl_opy_ (u"ࠬࡌࡁࡊࡎࠪඪ")
    ERROR = bstackl_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬණ")
    WARNING = bstackl_opy_ (u"ࠧࡘࡃࡕࡒࠬඬ")
    bstack1l11lll1l1_opy_ = bstackl_opy_ (u"ࠨࡋࡑࡊࡔ࠭ත")
    DEBUG = bstackl_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨථ")
    TRACE = bstackl_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩද")
    bstack1l11llll11_opy_ = [FAIL, ERROR]
def bstack1l11ll11ll_opy_(bstack1l11l11l11_opy_):
    if not bstack1l11l11l11_opy_:
        return None
    if bstack1l11l11l11_opy_.get(bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧධ"), None):
        return getattr(bstack1l11l11l11_opy_[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨන")], bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ඲"), None)
    return bstack1l11l11l11_opy_.get(bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬඳ"), None)
def bstack1l1l111ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧප"), bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫඵ")]:
        return
    if hook_type.lower() == bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩබ"):
        if current_test_uuid is None:
            return bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨභ")
        else:
            return bstackl_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪම")
    elif hook_type.lower() == bstackl_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨඹ"):
        if current_test_uuid is None:
            return bstackl_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪය")
        else:
            return bstackl_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬර")