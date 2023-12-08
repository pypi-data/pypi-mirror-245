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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1lll111_opy_, bstack1lllll111_opy_, bstack11l1l11ll_opy_, bstack1llll1ll1l_opy_, \
    bstack11l1lll1l1_opy_
def bstack1l111ll1_opy_(bstack111l111111_opy_):
    for driver in bstack111l111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l1ll111_opy_(driver, status, reason=bstackl_opy_ (u"ࠧࠨᎍ")):
    bstack1l1ll111l1_opy_ = Config.get_instance()
    if bstack1l1ll111l1_opy_.bstack1l111l1l11_opy_():
        return
    bstack1ll11l111_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᎎ"), bstackl_opy_ (u"ࠩࠪᎏ"), status, reason, bstackl_opy_ (u"ࠪࠫ᎐"), bstackl_opy_ (u"ࠫࠬ᎑"))
    driver.execute_script(bstack1ll11l111_opy_)
def bstack1l11l1ll1_opy_(page, status, reason=bstackl_opy_ (u"ࠬ࠭᎒")):
    try:
        if page is None:
            return
        bstack1l1ll111l1_opy_ = Config.get_instance()
        if bstack1l1ll111l1_opy_.bstack1l111l1l11_opy_():
            return
        bstack1ll11l111_opy_ = bstack11l11lll_opy_(bstackl_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ᎓"), bstackl_opy_ (u"ࠧࠨ᎔"), status, reason, bstackl_opy_ (u"ࠨࠩ᎕"), bstackl_opy_ (u"ࠩࠪ᎖"))
        page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ᎗"), bstack1ll11l111_opy_)
    except Exception as e:
        print(bstackl_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤ᎘"), e)
def bstack11l11lll_opy_(type, name, status, reason, bstack1ll1l111ll_opy_, bstack1l1l1lll_opy_):
    bstack1ll111l1_opy_ = {
        bstackl_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ᎙"): type,
        bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᎚"): {}
    }
    if type == bstackl_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ᎛"):
        bstack1ll111l1_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᎜")][bstackl_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᎝")] = bstack1ll1l111ll_opy_
        bstack1ll111l1_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᎞")][bstackl_opy_ (u"ࠫࡩࡧࡴࡢࠩ᎟")] = json.dumps(str(bstack1l1l1lll_opy_))
    if type == bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ꭰ"):
        bstack1ll111l1_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᎡ")][bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᎢ")] = name
    if type == bstackl_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᎣ"):
        bstack1ll111l1_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᎤ")][bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᎥ")] = status
        if status == bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᎦ") and str(reason) != bstackl_opy_ (u"ࠧࠨᎧ"):
            bstack1ll111l1_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᎨ")][bstackl_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᎩ")] = json.dumps(str(reason))
    bstack1ll11l1l11_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭Ꭺ").format(json.dumps(bstack1ll111l1_opy_))
    return bstack1ll11l1l11_opy_
def bstack111llll1l_opy_(url, config, logger, bstack1l1ll111ll_opy_=False):
    hostname = bstack1lllll111_opy_(url)
    is_private = bstack1llll1ll1l_opy_(hostname)
    try:
        if is_private or bstack1l1ll111ll_opy_:
            file_path = bstack11l1lll111_opy_(bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᎫ"), bstackl_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᎬ"), logger)
            if os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᎭ")) and eval(
                    os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᎮ"))):
                return
            if (bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᎯ") in config and not config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᎰ")]):
                os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭Ꮁ")] = str(True)
                bstack111l11111l_opy_ = {bstackl_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᎲ"): hostname}
                bstack11l1lll1l1_opy_(bstackl_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᎳ"), bstackl_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᎴ"), bstack111l11111l_opy_, logger)
    except Exception as e:
        pass
def bstack1111lll1_opy_(caps, bstack111l1111ll_opy_):
    if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭Ꮅ") in caps:
        caps[bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᎶ")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭Ꮇ")] = True
        if bstack111l1111ll_opy_:
            caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᎸ")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᎹ")] = bstack111l1111ll_opy_
    else:
        caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᎺ")] = True
        if bstack111l1111ll_opy_:
            caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᎻ")] = bstack111l1111ll_opy_
def bstack111l1ll111_opy_(bstack1l111lll1l_opy_):
    bstack111l1111l1_opy_ = bstack11l1l11ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᎼ"), bstackl_opy_ (u"࠭ࠧᎽ"))
    if bstack111l1111l1_opy_ == bstackl_opy_ (u"ࠧࠨᎾ") or bstack111l1111l1_opy_ == bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᎿ"):
        threading.current_thread().testStatus = bstack1l111lll1l_opy_
    else:
        if bstack1l111lll1l_opy_ == bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏀ"):
            threading.current_thread().testStatus = bstack1l111lll1l_opy_