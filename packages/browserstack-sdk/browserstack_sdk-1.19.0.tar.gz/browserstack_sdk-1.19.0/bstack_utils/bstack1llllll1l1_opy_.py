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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11llll1ll1_opy_ as bstack1l11111lll_opy_
from bstack_utils.helper import bstack111l11lll_opy_, bstack1ll1ll1111_opy_, bstack1l11111l1l_opy_, bstack11llll11ll_opy_, bstack11ll1lll_opy_, get_host_info, bstack11lllll11l_opy_, bstack11l111l1l_opy_, bstack1l1l11l11l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1l11l11l_opy_(class_method=False)
def _11lllllll1_opy_(driver, bstack1ll1ll11l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstackl_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬේ"): caps.get(bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫෛ"), None),
        bstackl_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪො"): bstack1ll1ll11l1_opy_.get(bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪෝ"), None),
        bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧෞ"): caps.get(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧෟ"), None),
        bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ෠"): caps.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ෡"), None)
    }
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ෢") + str(error))
  return response
def bstack1ll11111ll_opy_(config):
  return config.get(bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෣"), False) or any([p.get(bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ෤"), False) == True for p in config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෥")]])
def bstack1ll111lll_opy_(config, bstack11l1l1l11_opy_):
  try:
    if not bstack1ll1ll1111_opy_(config):
      return False
    bstack1l1111l11l_opy_ = config.get(bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ෦"), False)
    bstack1l111111l1_opy_ = config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෧")][bstack11l1l1l11_opy_].get(bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ෨"), None)
    if bstack1l111111l1_opy_ != None:
      bstack1l1111l11l_opy_ = bstack1l111111l1_opy_
    bstack1l1111111l_opy_ = os.getenv(bstackl_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ෩")) is not None and len(os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ෪"))) > 0 and os.getenv(bstackl_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ෫")) != bstackl_opy_ (u"ࠨࡰࡸࡰࡱ࠭෬")
    return bstack1l1111l11l_opy_ and bstack1l1111111l_opy_
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ෭") + str(error))
  return False
def bstack111lll1l_opy_(bstack11llllllll_opy_, test_tags):
  bstack11llllllll_opy_ = os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ෮"))
  if bstack11llllllll_opy_ is None:
    return True
  bstack11llllllll_opy_ = json.loads(bstack11llllllll_opy_)
  try:
    include_tags = bstack11llllllll_opy_[bstackl_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෯")] if bstackl_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ෰") in bstack11llllllll_opy_ and isinstance(bstack11llllllll_opy_[bstackl_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ෱")], list) else []
    exclude_tags = bstack11llllllll_opy_[bstackl_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬෲ")] if bstackl_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ෳ") in bstack11llllllll_opy_ and isinstance(bstack11llllllll_opy_[bstackl_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ෴")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥ෵") + str(error))
  return False
def bstack1l1llll11l_opy_(config, bstack11lllll111_opy_, bstack1l11111ll1_opy_):
  bstack11llll1lll_opy_ = bstack1l11111l1l_opy_(config)
  bstack1l1111l111_opy_ = bstack11llll11ll_opy_(config)
  if bstack11llll1lll_opy_ is None or bstack1l1111l111_opy_ is None:
    logger.error(bstackl_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ෶"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭෷"), bstackl_opy_ (u"࠭ࡻࡾࠩ෸")))
    data = {
        bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ෹"): config[bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭෺")],
        bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ෻"): config.get(bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭෼"), os.path.basename(os.getcwd())),
        bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧ෽"): bstack111l11lll_opy_(),
        bstackl_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ෾"): config.get(bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ෿"), bstackl_opy_ (u"ࠧࠨ฀")),
        bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨก"): {
            bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩข"): bstack11lllll111_opy_,
            bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฃ"): bstack1l11111ll1_opy_,
            bstackl_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨค"): __version__
        },
        bstackl_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧฅ"): settings,
        bstackl_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧฆ"): bstack11lllll11l_opy_(),
        bstackl_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧง"): bstack11ll1lll_opy_(),
        bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪจ"): get_host_info(),
        bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫฉ"): bstack1ll1ll1111_opy_(config)
    }
    headers = {
        bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩช"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧซ"),
    }
    config = {
        bstackl_opy_ (u"ࠬࡧࡵࡵࡪࠪฌ"): (bstack11llll1lll_opy_, bstack1l1111l111_opy_),
        bstackl_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧญ"): headers
    }
    response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠧࡑࡑࡖࡘࠬฎ"), bstack1l11111lll_opy_ + bstackl_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬฏ"), data, config)
    bstack11llll1l1l_opy_ = response.json()
    if bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪฐ")]:
      parsed = json.loads(os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫฑ"), bstackl_opy_ (u"ࠫࢀࢃࠧฒ")))
      parsed[bstackl_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ณ")] = bstack11llll1l1l_opy_[bstackl_opy_ (u"࠭ࡤࡢࡶࡤࠫด")][bstackl_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨต")]
      os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩถ")] = json.dumps(parsed)
      return bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠩࡧࡥࡹࡧࠧท")][bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨธ")], bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠫࡩࡧࡴࡢࠩน")][bstackl_opy_ (u"ࠬ࡯ࡤࠨบ")]
    else:
      logger.error(bstackl_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧป") + bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨผ")])
      if bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩฝ")] == bstackl_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫพ"):
        for bstack1l11111111_opy_ in bstack11llll1l1l_opy_[bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪฟ")]:
          logger.error(bstack1l11111111_opy_[bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬภ")])
      return None, None
  except Exception as error:
    logger.error(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨม") +  str(error))
    return None, None
def bstack1lllll1ll1_opy_():
  if os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫย")) is None:
    return {
        bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧร"): bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧฤ"),
        bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪล"): bstackl_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩฦ")
    }
  data = {bstackl_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬว"): bstack111l11lll_opy_()}
  headers = {
      bstackl_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬศ"): bstackl_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧษ") + os.getenv(bstackl_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧส")),
      bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧห"): bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬฬ")
  }
  response = bstack11l111l1l_opy_(bstackl_opy_ (u"ࠪࡔ࡚࡚ࠧอ"), bstack1l11111lll_opy_ + bstackl_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ฮ"), data, { bstackl_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ฯ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstackl_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢะ") + datetime.utcnow().isoformat() + bstackl_opy_ (u"࡛ࠧࠩั"))
      return {bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨา"): bstackl_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪำ"), bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫิ"): bstackl_opy_ (u"ࠫࠬี")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣึ") + str(error))
    return {
        bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ื"): bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷุ࠭"),
        bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦูࠩ"): str(error)
    }
def bstack11l1l111_opy_(caps, options):
  try:
    bstack11llll111l_opy_ = caps.get(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵฺࠪ"), {}).get(bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ฻"), caps.get(bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ฼"), bstackl_opy_ (u"ࠬ࠭฽")))
    if bstack11llll111l_opy_:
      logger.warn(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ฾"))
      return False
    browser = caps.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ฿"), bstackl_opy_ (u"ࠨࠩเ")).lower()
    if browser != bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩแ"):
      logger.warn(bstackl_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨโ"))
      return False
    browser_version = caps.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬใ"), caps.get(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧไ")))
    if browser_version and browser_version != bstackl_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ๅ") and int(browser_version.split(bstackl_opy_ (u"ࠧ࠯ࠩๆ"))[0]) <= 94:
      logger.warn(bstackl_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠸࠳ࠨ็"))
      return False
    if not options is None:
      bstack11llll11l1_opy_ = options.to_capabilities().get(bstackl_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹ่ࠧ"), {})
      if bstackl_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ้ࠧ") in bstack11llll11l1_opy_.get(bstackl_opy_ (u"ࠫࡦࡸࡧࡴ๊ࠩ"), []):
        logger.warn(bstackl_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴๋ࠢ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ์") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11llllll1l_opy_ = config.get(bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧํ"), {})
    bstack11llllll1l_opy_[bstackl_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ๎")] = os.getenv(bstackl_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ๏"))
    bstack1l11111l11_opy_ = json.loads(os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ๐"), bstackl_opy_ (u"ࠫࢀࢃࠧ๑"))).get(bstackl_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๒"))
    caps[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭๓")] = True
    if bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ๔") in caps:
      caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ๕")][bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๖")] = bstack11llllll1l_opy_
      caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๗")][bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ๘")][bstackl_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๙")] = bstack1l11111l11_opy_
    else:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ๚")] = bstack11llllll1l_opy_
      caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭๛")][bstackl_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๜")] = bstack1l11111l11_opy_
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ๝") +  str(error))
def bstack11ll1l1l_opy_(driver, bstack11lllll1l1_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11llllll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11llllll11_opy_ = False
      bstack11llllll11_opy_ = url.scheme in [bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰࠣ๞"), bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ๟")]
      if bstack11llllll11_opy_:
        if bstack11lllll1l1_opy_:
          logger.info(bstackl_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ๠"))
          driver.execute_async_script(bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡁࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜ࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࠩࠫࠣࡁࡃࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡘ࡚ࡁࡓࡖࡈࡈࠬ࠲ࠠࡧࡰ࠵࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡇࡑࡕࡇࡊࡥࡓࡕࡃࡕࡘࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴ࠲ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡗ࡙ࡇࡒࡕࡇࡇࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡨࡱࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ๡"))
          logger.info(bstackl_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠢ๢"))
        else:
          driver.execute_script(bstackl_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡈࡒࡖࡈࡋ࡟ࡔࡖࡒࡔࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ๣"))
      return bstack11lllll1l1_opy_
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ๤") + str(e))
    return False
def bstack11111ll11_opy_(driver, class_name, name, module_name, path, bstack1ll1ll11l1_opy_):
  try:
    bstack11llll1l11_opy_ = [class_name] if not class_name is None else []
    bstack1l111111ll_opy_ = {
        bstackl_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ๥"): True,
        bstackl_opy_ (u"ࠦࡹ࡫ࡳࡵࡆࡨࡸࡦ࡯࡬ࡴࠤ๦"): {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ๧"): name,
            bstackl_opy_ (u"ࠨࡴࡦࡵࡷࡖࡺࡴࡉࡥࠤ๨"): os.environ.get(bstackl_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ࠭๩")),
            bstackl_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ๪"): str(path),
            bstackl_opy_ (u"ࠤࡶࡧࡴࡶࡥࡍ࡫ࡶࡸࠧ๫"): [module_name, *bstack11llll1l11_opy_, name],
        },
        bstackl_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ๬"): _11lllllll1_opy_(driver, bstack1ll1ll11l1_opy_)
    }
    driver.execute_script(bstackl_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡀࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡯ࡳ࠯ࡴࡨࡷࠥࡃࠠ࡯ࡷ࡯ࡰࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࠬࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟࠱ࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡤࡨࡩࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡖࡕࡅࡓ࡙ࡐࡐࡔࡗࡉࡗ࠭ࠬࠡࠪࡨࡺࡪࡴࡴࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡷࡥࡵ࡚ࡲࡢࡰࡶࡴࡴࡸࡴࡦࡴࡇࡥࡹࡧࠠ࠾ࠢࡨࡺࡪࡴࡴ࠯ࡦࡨࡸࡦ࡯࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡩࡴ࠰ࡵࡩࡸࠦ࠽ࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡶࡤࡴ࡙ࡸࡡ࡯ࡵࡳࡳࡷࡺࡥࡳࡆࡤࡸࡦࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬࡹ࡮ࡩࡴ࠰ࡵࡩࡸ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡈࡒࡉ࠭ࠬࠡࡽࠣࡨࡪࡺࡡࡪ࡮࠽ࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟ࠣࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࠫࠥࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟࠱ࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠣࠤࠥ๭"), bstack1l111111ll_opy_)
    logger.info(bstackl_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣ๮"))
  except Exception as bstack11lllll1ll_opy_:
    logger.error(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ๯") + str(path) + bstackl_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤ๰") + str(bstack11lllll1ll_opy_))