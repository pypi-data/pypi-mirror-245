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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l1l1lll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l1l1l11l_opy_:
    def __init__(self, handler):
        self._11l1l111ll_opy_ = {}
        self._11l1l1ll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l1l111ll_opy_[bstackl_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪቮ")] = Module._inject_setup_function_fixture
        self._11l1l111ll_opy_[bstackl_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩቯ")] = Module._inject_setup_module_fixture
        self._11l1l111ll_opy_[bstackl_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩተ")] = Class._inject_setup_class_fixture
        self._11l1l111ll_opy_[bstackl_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫቱ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l1l11ll1_opy_(bstackl_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧቲ"))
        Module._inject_setup_module_fixture = self.bstack11l1l11ll1_opy_(bstackl_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ታ"))
        Class._inject_setup_class_fixture = self.bstack11l1l11ll1_opy_(bstackl_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ቴ"))
        Class._inject_setup_method_fixture = self.bstack11l1l11ll1_opy_(bstackl_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨት"))
    def bstack11l1l11l1l_opy_(self, bstack11l1l1l1l1_opy_, hook_type):
        meth = getattr(bstack11l1l1l1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1l1ll11_opy_[hook_type] = meth
            setattr(bstack11l1l1l1l1_opy_, hook_type, self.bstack11l1l1llll_opy_(hook_type))
    def bstack11l1l11l11_opy_(self, instance, bstack11l1l1l111_opy_):
        if bstack11l1l1l111_opy_ == bstackl_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦቶ"):
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥቷ"))
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢቸ"))
        if bstack11l1l1l111_opy_ == bstackl_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧቹ"):
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦቺ"))
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣቻ"))
        if bstack11l1l1l111_opy_ == bstackl_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢቼ"):
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨች"))
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥቾ"))
        if bstack11l1l1l111_opy_ == bstackl_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦቿ"):
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥኀ"))
            self.bstack11l1l11l1l_opy_(instance.obj, bstackl_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢኁ"))
    @staticmethod
    def bstack11l1ll111l_opy_(hook_type, func, args):
        if hook_type in [bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬኂ"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩኃ")]:
            _11l1l1lll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l1l1llll_opy_(self, hook_type):
        def bstack11l1ll1111_opy_(arg=None):
            self.handler(hook_type, bstackl_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨኄ"))
            result = None
            exception = None
            try:
                self.bstack11l1ll111l_opy_(hook_type, self._11l1l1ll11_opy_[hook_type], (arg,))
                result = Result(result=bstackl_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩኅ"))
            except Exception as e:
                result = Result(result=bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪኆ"), exception=e)
                self.handler(hook_type, bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪኇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫኈ"), result)
        def bstack11l1l1ll1l_opy_(this, arg=None):
            self.handler(hook_type, bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭኉"))
            result = None
            exception = None
            try:
                self.bstack11l1ll111l_opy_(hook_type, self._11l1l1ll11_opy_[hook_type], (this, arg))
                result = Result(result=bstackl_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧኊ"))
            except Exception as e:
                result = Result(result=bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኋ"), exception=e)
                self.handler(hook_type, bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨኌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩኍ"), result)
        if hook_type in [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ኎"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ኏")]:
            return bstack11l1l1ll1l_opy_
        return bstack11l1ll1111_opy_
    def bstack11l1l11ll1_opy_(self, bstack11l1l1l111_opy_):
        def bstack11l1l1l1ll_opy_(this, *args, **kwargs):
            self.bstack11l1l11l11_opy_(this, bstack11l1l1l111_opy_)
            self._11l1l111ll_opy_[bstack11l1l1l111_opy_](this, *args, **kwargs)
        return bstack11l1l1l1ll_opy_