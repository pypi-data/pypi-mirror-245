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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11lllll11l_opy_, bstack11ll1lll_opy_, get_host_info, bstack1l11111l1l_opy_, bstack11llll11ll_opy_, bstack11l1llllll_opy_, \
    bstack11l1ll11l1_opy_, bstack11ll1l1lll_opy_, bstack11l111l1l_opy_, bstack11l1llll1l_opy_, bstack11llll111_opy_, bstack1l1l11l11l_opy_
from bstack_utils.bstack111l11l1ll_opy_ import bstack111l1l1111_opy_
from bstack_utils.bstack1l11l111l1_opy_ import bstack1l11l1l1l1_opy_
bstack11111llll1_opy_ = [
    bstackl_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭᏿"), bstackl_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ᐀"), bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᐁ"), bstackl_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᐂ"),
    bstackl_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᐃ"), bstackl_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᐄ"), bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᐅ")
]
bstack11111ll1l1_opy_ = bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᐆ")
logger = logging.getLogger(__name__)
class bstack1lll11l1ll_opy_:
    bstack111l11l1ll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def launch(cls, bs_config, bstack11111ll1ll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1111l11ll1_opy_():
            return
        cls.bstack1111l11l1l_opy_()
        bstack11llll1lll_opy_ = bstack1l11111l1l_opy_(bs_config)
        bstack1l1111l111_opy_ = bstack11llll11ll_opy_(bs_config)
        data = {
            bstackl_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪᐇ"): bstackl_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩᐈ"),
            bstackl_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫᐉ"): bs_config.get(bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᐊ"), bstackl_opy_ (u"ࠧࠨᐋ")),
            bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐌ"): bs_config.get(bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᐍ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐎ"): bs_config.get(bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐏ")),
            bstackl_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᐐ"): bs_config.get(bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᐑ"), bstackl_opy_ (u"ࠧࠨᐒ")),
            bstackl_opy_ (u"ࠨࡵࡷࡥࡷࡺ࡟ࡵ࡫ࡰࡩࠬᐓ"): datetime.datetime.now().isoformat(),
            bstackl_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᐔ"): bstack11l1llllll_opy_(bs_config),
            bstackl_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭ᐕ"): get_host_info(),
            bstackl_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬᐖ"): bstack11ll1lll_opy_(),
            bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐗ"): os.environ.get(bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᐘ")),
            bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬᐙ"): os.environ.get(bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ᐚ"), False),
            bstackl_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫᐛ"): bstack11lllll11l_opy_(),
            bstackl_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᐜ"): {
                bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᐝ"): bstack11111ll1ll_opy_.get(bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᐞ"), bstackl_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᐟ")),
                bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᐠ"): bstack11111ll1ll_opy_.get(bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᐡ")),
                bstackl_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᐢ"): bstack11111ll1ll_opy_.get(bstackl_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᐣ"))
            }
        }
        config = {
            bstackl_opy_ (u"ࠫࡦࡻࡴࡩࠩᐤ"): (bstack11llll1lll_opy_, bstack1l1111l111_opy_),
            bstackl_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᐥ"): cls.default_headers()
        }
        response = bstack11l111l1l_opy_(bstackl_opy_ (u"࠭ࡐࡐࡕࡗࠫᐦ"), cls.request_url(bstackl_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᐧ")), data, config)
        if response.status_code != 200:
            os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᐨ")] = bstackl_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᐩ")
            os.environ[bstackl_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᐪ")] = bstackl_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᐫ")
            os.environ[bstackl_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᐬ")] = bstackl_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᐭ")
            os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᐮ")] = bstackl_opy_ (u"ࠣࡰࡸࡰࡱࠨᐯ")
            bstack1111l1ll11_opy_ = response.json()
            if bstack1111l1ll11_opy_ and bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᐰ")]:
                error_message = bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᐱ")]
                if bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᐲ")] == bstackl_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡎࡔࡖࡂࡎࡌࡈࡤࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࠪᐳ"):
                    logger.error(error_message)
                elif bstack1111l1ll11_opy_[bstackl_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᐴ")] == bstackl_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉ࠭ᐵ"):
                    logger.info(error_message)
                elif bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᐶ")] == bstackl_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡕࡇࡏࡤࡊࡅࡑࡔࡈࡇࡆ࡚ࡅࡅࠩᐷ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstackl_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᐸ"))
            return [None, None, None]
        logger.debug(bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᐹ"))
        os.environ[bstackl_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᐺ")] = bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫᐻ")
        bstack1111l1ll11_opy_ = response.json()
        if bstack1111l1ll11_opy_.get(bstackl_opy_ (u"ࠧ࡫ࡹࡷࠫᐼ")):
            os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᐽ")] = bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠩ࡭ࡻࡹ࠭ᐾ")]
            os.environ[bstackl_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᐿ")] = json.dumps({
                bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᑀ"): bstack11llll1lll_opy_,
                bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᑁ"): bstack1l1111l111_opy_
            })
        if bstack1111l1ll11_opy_.get(bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᑂ")):
            os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑃ")] = bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᑄ")]
        if bstack1111l1ll11_opy_.get(bstackl_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᑅ")):
            os.environ[bstackl_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᑆ")] = str(bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᑇ")])
        return [bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠬࡰࡷࡵࠩᑈ")], bstack1111l1ll11_opy_[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᑉ")], bstack1111l1ll11_opy_[bstackl_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᑊ")]]
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstackl_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᑋ")] == bstackl_opy_ (u"ࠤࡱࡹࡱࡲࠢᑌ") or os.environ[bstackl_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᑍ")] == bstackl_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᑎ"):
            print(bstackl_opy_ (u"ࠬࡋࡘࡄࡇࡓࡘࡎࡕࡎࠡࡋࡑࠤࡸࡺ࡯ࡱࡄࡸ࡭ࡱࡪࡕࡱࡵࡷࡶࡪࡧ࡭ࠡࡔࡈࡕ࡚ࡋࡓࡕࠢࡗࡓ࡚ࠥࡅࡔࡖࠣࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠣ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᑏ"))
            return {
                bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᑐ"): bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᑑ"),
                bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑒ"): bstackl_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᑓ")
            }
        else:
            cls.bstack111l11l1ll_opy_.shutdown()
            data = {
                bstackl_opy_ (u"ࠪࡷࡹࡵࡰࡠࡶ࡬ࡱࡪ࠭ᑔ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstackl_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᑕ"): cls.default_headers()
            }
            bstack11ll1l11l1_opy_ = bstackl_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭ᑖ").format(os.environ[bstackl_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᑗ")])
            bstack11111lllll_opy_ = cls.request_url(bstack11ll1l11l1_opy_)
            response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠧࡑࡗࡗࠫᑘ"), bstack11111lllll_opy_, data, config)
            if not response.ok:
                raise Exception(bstackl_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᑙ"))
    @classmethod
    def bstack1l1l11111l_opy_(cls):
        if cls.bstack111l11l1ll_opy_ is None:
            return
        cls.bstack111l11l1ll_opy_.shutdown()
    @classmethod
    def bstack11llll1l1_opy_(cls):
        if cls.on():
            print(
                bstackl_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬᑚ").format(os.environ[bstackl_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᑛ")]))
    @classmethod
    def bstack1111l11l1l_opy_(cls):
        if cls.bstack111l11l1ll_opy_ is not None:
            return
        cls.bstack111l11l1ll_opy_ = bstack111l1l1111_opy_(cls.bstack1111l11l11_opy_)
        cls.bstack111l11l1ll_opy_.start()
    @classmethod
    def bstack1l1l11ll1l_opy_(cls, bstack1l1l111l1l_opy_, bstack11111lll1l_opy_=bstackl_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᑜ")):
        if not cls.on():
            return
        bstack111l111l1_opy_ = bstack1l1l111l1l_opy_[bstackl_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᑝ")]
        bstack1111l111ll_opy_ = {
            bstackl_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᑞ"): bstackl_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫᑟ"),
            bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᑠ"): bstackl_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᑡ"),
            bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᑢ"): bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖ࡯࡮ࡶࡰࡦࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᑣ"),
            bstackl_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᑤ"): bstackl_opy_ (u"࠭ࡌࡰࡩࡢ࡙ࡵࡲ࡯ࡢࡦࠪᑥ"),
            bstackl_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᑦ"): bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑧ"),
            bstackl_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᑨ"): bstackl_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑩ"),
            bstackl_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᑪ"): bstackl_opy_ (u"ࠬࡉࡂࡕࡡࡘࡴࡱࡵࡡࡥࠩᑫ")
        }.get(bstack111l111l1_opy_)
        if bstack11111lll1l_opy_ == bstackl_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᑬ"):
            cls.bstack1111l11l1l_opy_()
            cls.bstack111l11l1ll_opy_.add(bstack1l1l111l1l_opy_)
        elif bstack11111lll1l_opy_ == bstackl_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᑭ"):
            cls.bstack1111l11l11_opy_([bstack1l1l111l1l_opy_], bstack11111lll1l_opy_)
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def bstack1111l11l11_opy_(cls, bstack1l1l111l1l_opy_, bstack11111lll1l_opy_=bstackl_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᑮ")):
        config = {
            bstackl_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᑯ"): cls.default_headers()
        }
        response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᑰ"), cls.request_url(bstack11111lll1l_opy_), bstack1l1l111l1l_opy_, config)
        bstack11llll1l1l_opy_ = response.json()
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def bstack1l11l11111_opy_(cls, bstack1l1l1l111l_opy_):
        bstack1111l1l11l_opy_ = []
        for log in bstack1l1l1l111l_opy_:
            bstack11111ll11l_opy_ = {
                bstackl_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᑱ"): bstackl_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧᑲ"),
                bstackl_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᑳ"): log[bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᑴ")],
                bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᑵ"): log[bstackl_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᑶ")],
                bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪᑷ"): {},
                bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑸ"): log[bstackl_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑹ")],
            }
            if bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑺ") in log:
                bstack11111ll11l_opy_[bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑻ")] = log[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑼ")]
            elif bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑽ") in log:
                bstack11111ll11l_opy_[bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑾ")] = log[bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑿ")]
            bstack1111l1l11l_opy_.append(bstack11111ll11l_opy_)
        cls.bstack1l1l11ll1l_opy_({
            bstackl_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᒀ"): bstackl_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᒁ"),
            bstackl_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᒂ"): bstack1111l1l11l_opy_
        })
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def bstack1111l1111l_opy_(cls, steps):
        bstack1111l11lll_opy_ = []
        for step in steps:
            bstack1111l111l1_opy_ = {
                bstackl_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᒃ"): bstackl_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬᒄ"),
                bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᒅ"): step[bstackl_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᒆ")],
                bstackl_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᒇ"): step[bstackl_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᒈ")],
                bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᒉ"): step[bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᒊ")],
                bstackl_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᒋ"): step[bstackl_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᒌ")]
            }
            if bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᒍ") in step:
                bstack1111l111l1_opy_[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᒎ")] = step[bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᒏ")]
            elif bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᒐ") in step:
                bstack1111l111l1_opy_[bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᒑ")] = step[bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒒ")]
            bstack1111l11lll_opy_.append(bstack1111l111l1_opy_)
        cls.bstack1l1l11ll1l_opy_({
            bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᒓ"): bstackl_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᒔ"),
            bstackl_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᒕ"): bstack1111l11lll_opy_
        })
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def bstack1ll1lll1l1_opy_(cls, screenshot):
        cls.bstack1l1l11ll1l_opy_({
            bstackl_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᒖ"): bstackl_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᒗ"),
            bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᒘ"): [{
                bstackl_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᒙ"): bstackl_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬᒚ"),
                bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᒛ"): datetime.datetime.utcnow().isoformat() + bstackl_opy_ (u"ࠬࡠࠧᒜ"),
                bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᒝ"): screenshot[bstackl_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᒞ")],
                bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᒟ"): screenshot[bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒠ")]
            }]
        }, bstack11111lll1l_opy_=bstackl_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒡ"))
    @classmethod
    @bstack1l1l11l11l_opy_(class_method=True)
    def bstack1ll111l111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l11ll1l_opy_({
            bstackl_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᒢ"): bstackl_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᒣ"),
            bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᒤ"): {
                bstackl_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᒥ"): cls.current_test_uuid(),
                bstackl_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢᒦ"): cls.bstack1l1l11l1ll_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstackl_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᒧ"), None) is None or os.environ[bstackl_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒨ")] == bstackl_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒩ"):
            return False
        return True
    @classmethod
    def bstack1111l11ll1_opy_(cls):
        return bstack11llll111_opy_(cls.bs_config.get(bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᒪ"), False))
    @staticmethod
    def request_url(url):
        return bstackl_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᒫ").format(bstack11111ll1l1_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstackl_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᒬ"): bstackl_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᒭ"),
            bstackl_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᒮ"): bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨᒯ")
        }
        if os.environ.get(bstackl_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒰ"), None):
            headers[bstackl_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᒱ")] = bstackl_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᒲ").format(os.environ[bstackl_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠣᒳ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᒴ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᒵ"), None)
    @staticmethod
    def bstack1l1l1l1ll1_opy_():
        if getattr(threading.current_thread(), bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᒶ"), None):
            return {
                bstackl_opy_ (u"ࠫࡹࡿࡰࡦࠩᒷ"): bstackl_opy_ (u"ࠬࡺࡥࡴࡶࠪᒸ"),
                bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᒹ"): getattr(threading.current_thread(), bstackl_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᒺ"), None)
            }
        if getattr(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᒻ"), None):
            return {
                bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᒼ"): bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᒽ"),
                bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᒾ"): getattr(threading.current_thread(), bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᒿ"), None)
            }
        return None
    @staticmethod
    def bstack1l1l11l1ll_opy_(driver):
        return {
            bstack11ll1l1lll_opy_(): bstack11l1ll11l1_opy_(driver)
        }
    @staticmethod
    def bstack1111l1l111_opy_(exception_info, report):
        return [{bstackl_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᓀ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1111l1l1_opy_(typename):
        if bstackl_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᓁ") in typename:
            return bstackl_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᓂ")
        return bstackl_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᓃ")
    @staticmethod
    def bstack1111l11111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11l1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1l1ll11l_opy_(test, hook_name=None):
        bstack1111l1l1l1_opy_ = test.parent
        if hook_name in [bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᓄ"), bstackl_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᓅ"), bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᓆ"), bstackl_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᓇ")]:
            bstack1111l1l1l1_opy_ = test
        scope = []
        while bstack1111l1l1l1_opy_ is not None:
            scope.append(bstack1111l1l1l1_opy_.name)
            bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l1ll_opy_(hook_type):
        if hook_type == bstackl_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᓈ"):
            return bstackl_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᓉ")
        elif hook_type == bstackl_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᓊ"):
            return bstackl_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᓋ")
    @staticmethod
    def bstack11111lll11_opy_(bstack11l1111l_opy_):
        try:
            if not bstack1lll11l1ll_opy_.on():
                return bstack11l1111l_opy_
            if os.environ.get(bstackl_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᓌ"), None) == bstackl_opy_ (u"ࠧࡺࡲࡶࡧࠥᓍ"):
                tests = os.environ.get(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᓎ"), None)
                if tests is None or tests == bstackl_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᓏ"):
                    return bstack11l1111l_opy_
                bstack11l1111l_opy_ = tests.split(bstackl_opy_ (u"ࠨ࠮ࠪᓐ"))
                return bstack11l1111l_opy_
        except Exception as exc:
            print(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᓑ"), str(exc))
        return bstack11l1111l_opy_
    @classmethod
    def bstack1l11l1ll1l_opy_(cls, event: str, bstack1l1l111l1l_opy_: bstack1l11l1l1l1_opy_):
        bstack1l1l111l11_opy_ = {
            bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᓒ"): event,
            bstack1l1l111l1l_opy_.bstack1l11l11ll1_opy_(): bstack1l1l111l1l_opy_.bstack1l1l1l1l11_opy_(event)
        }
        bstack1lll11l1ll_opy_.bstack1l1l11ll1l_opy_(bstack1l1l111l11_opy_)