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
import json
import logging
logger = logging.getLogger(__name__)
class bstack1l1ll1111l_opy_:
    def bstack1l1l1llll1_opy_():
        bstack1l1ll11111_opy_ = {}
        try:
            bstack1l1l1lll1l_opy_ = json.loads(os.environ[bstackl_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫೝ")])
            bstack1111l1ll_opy_ = os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬೞ"))
            if bstack1111l1ll_opy_ is not None and eval(bstack1111l1ll_opy_):
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ೟")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧೠ")]
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦೡ")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧೢ")]
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦೣ")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ೤")]
            else:
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠦࡴࡹࠢ೥")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠧࡵࡳࠣ೦")]
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ೧")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ೨")]
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ೩")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ೪")]
                bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦ೫")] = bstack1l1l1lll1l_opy_[bstackl_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ೬")]
            bstack1l1ll11111_opy_[bstackl_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ೭")] = bstack1l1l1lll1l_opy_.get(bstackl_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ೮"), None)
        except Exception as error:
            logger.error(bstackl_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨ೯") +  str(error))
        return bstack1l1ll11111_opy_