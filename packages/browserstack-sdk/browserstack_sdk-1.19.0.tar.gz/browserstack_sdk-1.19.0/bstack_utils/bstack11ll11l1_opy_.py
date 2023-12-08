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
import re
from bstack_utils.bstack1ll1l1l1_opy_ import bstack111l1ll111_opy_
def bstack111l1ll11l_opy_(fixture_name):
    if fixture_name.startswith(bstackl_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፚ")):
        return bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ፛")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ፜")):
        return bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ፝")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ፞")):
        return bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ፟")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ፠")):
        return bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ፡")
def bstack111l1l1l11_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ።"), fixture_name))
def bstack111l1lll11_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ፣"), fixture_name))
def bstack111l1ll1ll_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ፤"), fixture_name))
def bstack111l1l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstackl_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ፥")):
        return bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ፦"), bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ፧")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ፨")):
        return bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ፩"), bstackl_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ፪")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭፫")):
        return bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭፬"), bstackl_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ፭")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ፮")):
        return bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ፯"), bstackl_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ፰")
    return None, None
def bstack111l1l1ll1_opy_(hook_name):
    if hook_name in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭፱"), bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ፲")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1lllll_opy_(hook_name):
    if hook_name in [bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ፳"), bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ፴")]:
        return bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ፵")
    elif hook_name in [bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ፶"), bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ፷")]:
        return bstackl_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ፸")
    elif hook_name in [bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ፹"), bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ፺")]:
        return bstackl_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ፻")
    elif hook_name in [bstackl_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭፼"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭፽")]:
        return bstackl_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ፾")
    return hook_name
def bstack111ll1111l_opy_(node, scenario):
    if hasattr(node, bstackl_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ፿")):
        parts = node.nodeid.rsplit(bstackl_opy_ (u"ࠣ࡝ࠥᎀ"))
        params = parts[-1]
        return bstackl_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᎁ").format(scenario.name, params)
    return scenario.name
def bstack111l1llll1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstackl_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᎂ")):
            examples = list(node.callspec.params[bstackl_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᎃ")].values())
        return examples
    except:
        return []
def bstack111l1lll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1l1l_opy_(report):
    try:
        status = bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᎄ")
        if report.passed or (report.failed and hasattr(report, bstackl_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᎅ"))):
            status = bstackl_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᎆ")
        elif report.skipped:
            status = bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᎇ")
        bstack111l1ll111_opy_(status)
    except:
        pass
def bstack1l111111_opy_(status):
    try:
        bstack111l1ll1l1_opy_ = bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᎈ")
        if status == bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᎉ"):
            bstack111l1ll1l1_opy_ = bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᎊ")
        elif status == bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᎋ"):
            bstack111l1ll1l1_opy_ = bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᎌ")
        bstack111l1ll111_opy_(bstack111l1ll1l1_opy_)
    except:
        pass
def bstack111ll11111_opy_(item=None, report=None, summary=None, extra=None):
    return